import sublime, sublime_plugin
import urllib

ST3 = sublime.version() == '' or int(sublime.version()) > 3000
SET_NAME = "QueryTidier.sublime-settings"
SPLIT_KEY = "split_chars"
settings = sublime.load_settings(SET_NAME)

def selections(view, default_to_all=True):
    """Return all non-empty selections in view
    If None, return entire view if default_to_all is True
    """
    regions = [r for r in view.sel() if not r.empty()]

    if not regions and default_to_all:
        regions = [sublime.Region(0, view.size())]

    return regions

def decode(input):
	return urllib.parse.quote(input)

def encode (input):
	return urllib.parse.unquote(input)


class QuerytidiertidyCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		splits = settings.get(SPLIT_KEY)
		print(splits)
		view = self.view
		for region in selections(view):
			s = view.substr(region)
			view.replace(edit, region, decode(s))


class QuerytidierclutterCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		splits = settings.get(SPLIT_KEY)
		print(splits)
		view = self.view
		for region in selections(view):
			s = view.substr(region)
			s = encode(s)
			parsed = urllib.parse.urlparse(s)
			output = ""
			output += parsed.scheme + "\n"
			output += parsed.netloc + "\n"
			output += parsed.path + "\n"
			output += parsed.params + "\n"
			output += parsed.query + "\n"
			output += parsed.fragment + "\n"
			view.replace(edit, region, output)