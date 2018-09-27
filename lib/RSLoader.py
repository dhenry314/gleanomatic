import RSRestClient
import GleanomaticErrors

# RSLoader - add external resources and capabilities to an ResourceSync endpoint


class RSLoader:

    targetURI = None   
    targetEndpoint = None
    sourceNamespace = None
    capabilitiesPath = None
    client = None
    createDump = False

    def __init__(self,targetURI,sourceNamespace,capabilitiesPath,**kwargs):
        self.targetURI = targetURI
        self.targetEndpoint = RSRestClient(self.targetURI)
        self.sourceNamespace = sourceNamespace
        self.capabilitiesPath = capabilitiesPath
        self.createDump = True
        for key, value in kwargs.items():
            setattr(self, key, value)

    def run(self):
        pass

    def addResource(self,uri,setNamespace):
        try:
            self.targetEndpoint.addResource(uri,self.sourceNamespace,setNamespace)
        except BadResourceURI as e:
            raise ValueError("Could not load resource at " + str(uri))
        if self.createDump:
            self.addToDump(uri,self.sourceNamespace,setNamespace,content)

    def deleteResource(self,uri,setNamespace):
        pass

    def addCapability(self,uri,setNamespace):
        pass
