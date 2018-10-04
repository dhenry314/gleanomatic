# RSRestClient - client to interact with a RSEngine REST endpoint
import urllib.request
import urllib.parse
from GleanomaticErrors import BadResourceURL, AddResourceError


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

        
    def checkURI(self,uri):
        try:
            with urllib.request.urlopen(uri) as response:
                content = response.read()
        except (urllib.error.HTTPError, urllib.error.URLError, ValueError) as e:
            raise BadResourceURL(uri,e)
        return True
            
    def addResource(self,uri,sourceNamespace,setNamespace):
        try:
            self.checkURI(uri)
        except BadResourceURL as e:
            raise Exception("Resource uri did not validate. uri: " + str(uri))
        data = urllib.parse.urlencode({'sourceNamespace' : sourceNamespace, 'setNamespace' : setNamespace, 'uri': uri}).encode("utf-8")
        req = urllib.request.Request(self.resourceURI, data=data)
        response = urllib.request.urlopen(req)
        d = response.read()
        return d
        
    def deleteResource(self,uri):
        headers = {
            'Content-Type': 'application/json;charset=UTF-8'
        }
        try:
            req = urllib.request.Request(
                uri,
                headers=headers,
                method='DELETE'
            )
            response = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            raise BadResourceURL(uri,e)
        d = response.read()
        return d

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

