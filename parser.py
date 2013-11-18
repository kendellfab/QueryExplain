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

def getOutput(input):
	parsed = urllib.parse.urlparse(input)
	output = ""
	output += parsed.scheme + "://"
	output += parsed.netloc + ""
	output += parsed.path
	output += parsed.params + "\n"
	query = urllib.parse.parse_qs(parsed.query)
	print(query)
	for key, val in query.items():
		for item in val:
			output += "\t&" + key + "=" + formatValue(item) + "\n"
	output += parsed.fragment + "\n"
	return output


def formatValue(value):
	splits = settings.get(SPLIT_KEY)
	result = value
	insert = "\n\t\t"
	for split in splits:
		parts = result.split(split)
		result = insert.join(parts)

	return result

def insert(original, new, pos):
  '''Inserts new inside original at pos.'''
  return original[:pos] + new + original[pos:]
 

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
		view = self.view
		for region in selections(view):
			s = view.substr(region)
			s = encode(s)
			sz = region.end()
			view.insert(edit, sz, "\n\n"+getOutput(s)+"\n")