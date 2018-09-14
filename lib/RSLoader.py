import RSClient

# RSLoader - add external resources and capabilities to an ResourceSync endpoint


class RSLoader:

    targetURI = None   
    targetEndpoint = None
    capabilitiesPath = None

    def __init__(self,targetURI,capabilitiesPath):
        self.targetURI = targetURI
        self.targetEndpoint = RSClient(self.targetURI)
        self.capabilitiesPath = capabilitiesPath


    def addResource(self,uri,setNamespace):
        pass

    def deleteResource(self,uri,setNamespace):
        pass

    def addCapability(self,uri,setNamespace):
        pass
