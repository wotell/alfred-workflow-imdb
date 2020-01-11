import sys
import urllib2
import json
from workflow import Workflow, ICON_WEB

WORKFLOW_MODE = bool(True)
IMDB_BASE_WEBSITE_URL = 'https://www.imdb.com'
IMDB_MOVIE_URL = IMDB_BASE_WEBSITE_URL + '/title/{id}/'
IMDB_ACTOR_URL = IMDB_BASE_WEBSITE_URL + '/name/{id}/'
IMDB_BASE_API_URL = 'https://sg.media-imdb.com'
IMDB_SUGGESTIONS_URL = IMDB_BASE_API_URL + '/suggestion/{firstchar}/{query}.json'

class Suggestion:
    title = ''
    id = ''
    url = ''
    shortinfo = ''
    valid = bool(True)

def getSuggestions(query):
    firstchar = query[0]
    url = IMDB_SUGGESTIONS_URL.format(firstchar=firstchar, query=query)
    reply = urllib2.urlopen(url).read()
    parsed = json.loads(reply)
    result = []
    for imdbResult in parsed['d']:
        suggestion = Suggestion()
        suggestion.title = imdbResult['l']
        suggestion.id = imdbResult['id']
        suggestion.shortinfo = imdbResult['s']
        if (suggestion.id.startswith('tt')):
            suggestion.url = IMDB_MOVIE_URL.format(id=suggestion.id)
        elif (suggestion.id.startswith('nm')):
            suggestion.url = IMDB_ACTOR_URL.format(id=suggestion.id)
        else:
            suggestion.valid = bool(False)

        result.append(suggestion)

    return result

def suggestionsToWorkflow(suggestions):
    debug('Feedback for Alfred:')
    for suggestion in suggestions:
        debug(suggestion.title + '(valid:{valid})'.format(valid=suggestion.valid))
        wf.add_item(title=suggestion.title,
                    subtitle=suggestion.shortinfo,
                    arg=suggestion.url,
                    valid=str(suggestion.valid),
                    icon=ICON_WEB)
    wf.send_feedback()

def debug(message):
    if not WORKFLOW_MODE:
        print message

def main(wf):
    query = sys.argv[1]
    suggestions = getSuggestions(query)
    suggestionsToWorkflow(suggestions)

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))