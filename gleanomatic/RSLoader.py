import os
import json
from multiprocessing import Pool 
from datetime import datetime
import time

from gleanomatic.configure import appConfig
import gleanomatic.RSRestClient as rc
import gleanomatic.Utils as Utils
from gleanomatic.GleanomaticErrors import BadResourceURL, RSPathException, TargetURIException, AddDumpException
import gleanomatic.gleanomaticLogger as gl

logger = gl.logger

# RSLoader - add external resources and capabilities to an ResourceSync endpoint


class RSLoader:

    targetURI = None   
    targetEndpoint = None
    sourceNamespace = None
    setNamespace = None
    client = None
    createDump = False
    batchTag = None
    addCount = 0
    warnings = 0

    def __init__(self,sourceNamespace,setNamespace,opts={}):
        logger.info("Initializing RSLoader")
        self.targetURI = appConfig.targetURI
        self.targetEndpoint = rc.RSRestClient(self.targetURI)
        self.sourceNamespace = sourceNamespace
        self.setNamespace = setNamespace
        self.createDump = appConfig.createDump
        now = datetime.now()
        self.batchTag = str(now.year)+str(now.month).zfill(2)+str(now.day).zfill(2)+str(now.hour).zfill(2)+str(now.minute).zfill(2)
        for key, value in opts.items():
            setattr(self, key, value)

    def run(self):
        pass

    def addResource(self,uri):
        contents, message = self.targetEndpoint.addResource(uri,self.sourceNamespace,self.setNamespace,self.batchTag)
        batchTag = Utils.getRecordAttr(contents,'batchTag')
        if batchTag == self.batchTag:
            self.addCount = self.addCount + 1
        if message:
            self.warnings = self.warnings + 1
        return contents
        
    def addBatch(self, uris):
        pool = Pool()
        pool.map(self.addResource, uris)
        pool.close() 
        pool.join()
        
    def deleteResource(self,uri):
        pass

    def addCapability(self,url,capType):
        contents, message = self.targetEndpoint.addCapability(url,self.sourceNamespace,self.setNamespace,capType)
        return contents
    
    def makeDump(self):
        if self.createDump:
            contents = self.targetEndpoint.addDump(self.batchTag,self.sourceNamespace,self.setNamespace)
            #zipURI = json.loads(contents)
            zipURI = contents
            logger.info("zipURI: " + str(zipURI))
            while True:
                retries = 0
                try:
                    uriResponse = Utils.checkURI(zipURI)
                except Exception as e:
                    logger.info("Exception from checkURI: " + str(e))
                    #allow up to 1 hour for zip creation - sleep 60 seconds and try 60 times
                    time.sleep(60)
                    retries = retries + 1
                    if retries > 60:
                        logger.critical("Too many retries waiting for " + str(zipURI))
                        raise AddDumpException("Too many retries waiting for " + str(zipURI))
                    continue
                if uriResponse:
                    logger.info("Found zipURI.")
                    break
            result = self.addCapability(zipURI,'dump')    
            return result
        return False
        
    def getSummary(self):
        return str(self.addCount) + " new/updated records loaded. " + str(self.warnings) + " warnings. "

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)

