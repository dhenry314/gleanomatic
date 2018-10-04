# Common Utils
import urllib.request
import urllib.parse
from GleanomaticErrors import URIException

def checkURI(uri):
    try:
        with urllib.request.urlopen(uri) as response:
            content = response.read()
    except (urllib.error.HTTPError, urllib.error.URLError, ValueError) as e:
        raise URIException(uri,e)
    finally:
        return True

def validateRequired(opts,required):
    for key in required:
        if key not in opts:
            raise ValueError(str(key) + " is required!")
    return True

def getContent(url):
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read()
    except:
        raise ValueError("Could not load content from url: " + str(url))
    return content
 