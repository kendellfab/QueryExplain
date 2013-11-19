import sublime, sublime_plugin
import urllib

ST3 = sublime.version() == '' or int(sublime.version()) > 3000
SET_NAME = "QueryExplain.sublime-settings"
SPLIT_KEY = "split_chars"

NL = "\n"
TAB = "\t"


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
	output += parsed.params + NL
	query = urllib.parse.parse_qs(parsed.query)
	print(query)
	for key, val in query.items():
		for item in val:
			output += TAB + "&" + key + "=" + formatValue(item) + NL
	output += parsed.fragment
	return output


def formatValue(value):
	settings = sublime.load_settings(SET_NAME)
	splits = settings.get(SPLIT_KEY)
	result = value
	insert = NL + TAB + TAB
	for split in splits:		
		start = result.find(split, 0)
		while start != -1:
			result = insertText(result, insert, start)
			start = result.find(split, start  + len(split) + len(insert))

	return result

def insertText(original, new, pos):
  return original[:pos] + new + original[pos:]


class QuerycondenseCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		for region in selections(view):
			s = view.substr(region)
			result = s.replace(NL, "").replace(TAB, "").replace(" ", "+").replace("&", "?", 1)
			view.replace(edit, region, result)


class QueryexplainCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		for region in selections(view):
			s = view.substr(region)
			s = encode(s)
			sz = region.end()
			view.replace(edit, region, getOutput(s))