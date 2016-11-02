import sublime, sublime_plugin, re, urllib.parse, urllib.request, webbrowser

class FileToGoPlaygroundCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    syntax = re.search('\/.*\/', self.view.settings().get('syntax')).group(0).replace('/', '')

    if (syntax.lower() != "go"):
      sublime.error_message('You can only send Go code to the playground.')
      return
    
    selection = self.view.substr(self.view.visible_region()).encode('ascii')

    req = urllib.request.Request('https://play.golang.org/share', selection)
    try:
      with urllib.request.urlopen(req) as response:
         shareID = response.read().decode("utf-8")
    except urllib.error.URLError:
      sublime.error_message('Something went wrong, is your internet ok?')
      return
    sendToBrowser(shareID)

def sendToBrowser(shareID):
  webbrowser.open("https://play.golang.org/p/" + shareID)