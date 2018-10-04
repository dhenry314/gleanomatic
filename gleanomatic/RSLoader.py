import os
from datetime import datetime
from configure import appConfig
import RSRestClient as rc
import Utils
import json
from GleanomaticErrors import BadResourceURL, RSPathException, TargetURIException

# RSLoader - add external resources and capabilities to an ResourceSync endpoint


class RSLoader:

    targetURI = None   
    targetEndpoint = None
    sourceNamespace = None
    setNamespace = None
    RSPath = None
    client = None
    createDump = False
    batchTag = None

    def __init__(self,sourceNamespace,setNamespace,opts):
        self.RSPath = appConfig.RSPath
        if os.access(self.RSPath, os.W_OK) is not True:
            raise RSPathException("RSPath not writable")
        self.targetURI = appConfig.targetURI
        try:
            Utils.checkURI(str(self.targetURI) + "/resource" )
        except Exception as e:
            raise TargetURIException("TargetURI did not validate: " + str(self.targetURI) + "/resource" ,e)
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
        contents = self.targetEndpoint.addResource(uri,self.sourceNamespace,self.setNamespace)
        result = json.loads(contents)
        if self.createDump:
            self.addToDump(uri,content,)

    def deleteResource(self,uri):
        pass

    def addCapability(self,uri):
        pass
    
    def addToDump(self,uri,content):
        #set initial path
        path = str(self.RSPath) + "/" + str(self.sourceNamespace) + "/" + str(self.setNamespace) + "/" + str(self.batchTag)
        if not os.path.isdir(path):
            os.makedirs( path, 777 )

