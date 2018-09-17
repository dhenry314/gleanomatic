# RSRestClient - client to interact with a RSEngine REST endpoint
import urllib.request
import urllib.parse

class RSRestClient:

    endpointURI = None
    resourceURI = None
    capabilityURI = None 

    def __init__(self,endpointURI):
        #ensure that there is a trailing slash on the endpoint
        if endpointURI[-1] != "/":
            endpointURI = str(endpointURI) + "/" 
        self.endpointURI = endpointURI
        self.resourceURI = str(self.endpointURI) + "resource"
        self.capabilityURI = str(self.endpointURI) + "capability"
        

    def addResource(self,uri,sourceNamespace,setNamespace):
        data = urllib.parse.urlencode({'sourceNamespace' : sourceNamespace, 'setNamespace' : setNamespace, 'uri': uri}).encode("utf-8")
        req = urllib.request.Request(self.resourceURI, data=data)
        response = urllib.request.urlopen(req)
        d = response.read()
        print(d)
        
    def deleteResource(self,uri,sourceNamespace,setNamespace):
        pass

    def getResources(self,**kwargs):
        url = self.endpointURI + str("resource")
        print(url)
        f = urllib.request.urlopen(url)
        print(f.read().decode('utf-8'))

    def addCapability(self,capURL,sourceNamespace,setNamespace,capType):
        pass

    def deleteCapability(self,capURL,sourceNamespace,setNamespace):
        pass

    def getCapabilities(self,**kwargs):
        pass

    def what(self):
        print("This is a RSRestClient.")

