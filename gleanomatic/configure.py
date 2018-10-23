import os
import urllib.request

class appConfig:
    RSPath = "/home/dhenry/Dev/RSEngine/app/app/static/"
    targetURI = "http://resourcesync"
    createDump = True
    logDir = os.environ['LOG_DEST']
    logFile = os.environ['LOG_FILE']
    logLevel = os.environ['LOG_LEVEL']
    logURL = os.environ['LOG_URL']
    userAgent = os.environ['USER_AGENT']
