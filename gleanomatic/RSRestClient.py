# RSRestClient - client to interact with a RSEngine REST endpoint
import urllib.request
import urllib.parse
import json

import gleanomatic.Utils as Utils
from gleanomatic.GleanomaticErrors import BadResourceURL, AddResourceError, AddDumpException

class RSRestClient:

    endpointURI = None
    resourceURI = None
    capabilityURI = None
    logger = None 

    def __init__(self,endpointURI,logger):
        self.logger = logger
        self.logger.info("Initializing RSRestClient")
        #ensure that there is a trailing slash on the endpoint
        if endpointURI[-1] != "/":
            endpointURI = str(endpointURI) + "/" 
        self.endpointURI = endpointURI
        self.resourceURI = str(self.endpointURI) + "resource"
        self.logger.info("Checking resourceURI: " + str(self.resourceURI))
        try:
            Utils.checkURI(self.resourceURI)
        except Exception as e:
            self.logger.critical("ResourceURI did not validate: " + str(self.resourceURI) + " ERROR:" + str(e))
            raise TargetURIException("ResourceURI did not validate: " + str(self.resourceURI) ,e)
        self.capabilityURI = str(self.endpointURI) + "capability"

        
    def getMessage(self,record):
        message = Utils.getRecordAttr(record,'message')
        msg = Utils.getRecordAttr(record,'msg')
        if message:
            return message
        if msg:
            return msg
        return None
   
    def addResource(self,uri,sourceNamespace,setNamespace,batchTag=None):
        self.logger.info("Adding resource with uri: " + str(uri))
        record = None
        message = None
        try:
            Utils.checkURI(uri)
        except URIException as e:
            raise Exception("Resource uri did not validate. uri: " + str(uri))
        params = {'sourceNamespace' : sourceNamespace, 'setNamespace' : setNamespace, 'uri': uri}
        if batchTag:
            params['batchTag'] = batchTag
        try:
            response = Utils.postRSData(self.resourceURI,params)
        except Exception as e:
            raise BadResourceURL("Could not add resource. resourceURI: " + str(self.resourceURI), e)
        record = Utils.getJSONFromResponse(response)
        message = self.getMessage(record) 
        if message:
            self.logger.warning(message)
        return record, message
        
    def addDump(self,batchTag,sourceNamespace,setNamespace):
        response = None
        params = {'sourceNamespace' : sourceNamespace, 'setNamespace' : setNamespace, 'batchTag': batchTag}
        try:
            response = Utils.postRSData(self.capabilityURI,params)
        except Exception as e:
            raise AddDumpException("Could not post dump.",e)
        d = Utils.getJSONFromResponse(response)
        d = self.convertToRSDomain(d)
        return d
 
    def convertToRSDomain(self,url):
        if ('://localhost:' in str(url)) or ('://localhost/' in str(url)):
            parts = str(url).split('/')
            subURL = '/'.join(parts[3:])
            url = 'http://resourcesync/' + str(subURL)
        return url
        
    def deleteResource(self,uri):
        response = Utils.deleteContent(uri)
        if not response:
            raise Exception("Could not delete resource at " + str(uri))
        d = response.read()
        return d

    def getResources(self,offset=0,count=20):
        url = self.endpointURI + str("resource")
        url = str(url) + "?offset=" + str(offset) + "&count=" + str(count)
        urlCheck = Utils.checkURI(url)
        if not urlCheck:
            return False
        f = urllib.request.urlopen(url)
        contents = Utils.getContent(url)
        return contents
        
    def getManifest(self,batchTag,sourceNamespace,setNamespace):
        url = self.endpointURI + "/static/" + str(sourceNamespace) + "/" + str(setNamespace) + "/" + str(batchTag) + "/manifest"
        urlCheck = Utils.checkURI(url)
        if not urlCheck:
            return False
        contents = Utils.getContent(url)
        return contents

    def addCapability(self,capURL,sourceNamespace,setNamespace,capType):
        self.logger.info("Adding capability with url:" + str(capURL))
        record = None
        message = None
        try:
            Utils.checkURI(capURL)
        except Exception as e:
            self.logger.warning("Capability URL did not validate. url: " + str(capURL) + " ERROR: "  + str(e))
            raise Exception("Capability URL did not validate. url: " + str(capURL) + " ERROR: "  + str(e))
        params = {'sourceNamespace' : sourceNamespace, 'setNamespace' : setNamespace, 'uri': capURL, 'capabilityType':capType}
        try:
            response = Utils.postRSData(self.capabilityURI,params)
        except Exception as e:
            self.logger.critical("Could not add capability. capabiltyURI: " + str(self.capabilityURI) + " ERROR: " + str(e))
            raise BadResourceURL(str(e))
        record = Utils.getJSONFromResponse(response)
        message = self.getMessage(record) 
        if message:
            self.logger.warning(message)
        return record, message
        
    def loadResourceListIndex(self,sourceNamespace,setNamespace):
        url = self.endpointURI + "/RS/" + str(sourceNamespace) + "/" + str(setNamespace) + "/resourcelistindex.json"
        urlCheck = Utils.checkURI(url)
        if not urlCheck:
            return False
        response = Utils.getResponse(url)
        data = Utils.getJSONFromResponse(response)
        urls = []
        if 'sitemapindex' in data:
            if 'sitemap' in data['sitemapindex']:
                sitemap = data['sitemapindex']['sitemap']
                for record in sitemap:
                    if 'rs:ln' in record:
                        if '@type' in record['rs:ln']:
                            if str(record['rs:ln']['@type']).lower() == 'application/json':
                                urls.append(record['rs:ln']['@href'])
        return urls

    #return a list of resource IDs from a given resourcelist url
    def loadResourceListIDs(self,url):
        url = self.convertToRSDomain(url)
        urlCheck = Utils.checkURI(url)
        if not urlCheck:
            return False
        response = Utils.getResponse(url)
        data = Utils.getJSONFromResponse(response)
        ids = []
        if 'urlset' in data:
            if 'url' in data['urlset']:
                urls = data['urlset']['url']
                for record in urls:
                    if 'rs:ln' in record:
                        if 'rel' in record['rs:ln']:
                            if str(record['rs:ln']['rel']).lower() == 'describedby':
                                resourceID = record['rs:ln']['href']
                                resourceID = resourceID.replace('/resource/','')
                                ids.append(resourceID)
        return ids
        
    def loadCapabilityList(self,sourceNamespace,setNamespace):
        url = self.endpointURI + "/RS/" + str(sourceNamespace) + "/" + str(setNamespace) + "/capabilitylist.json"
        urlCheck = Utils.checkURI(url)
        if not urlCheck:
            return False
        response = Utils.getResponse(url)
        data = Utils.getJSONFromResponse(response)
        if 'urlset' in data:
            if 'url' in data['urlset']:
                return data['urlset']['url']
        return []

    def loadManifestIDs(self,sourceNamespace,setNamespace,batchTag):
        url = self.endpointURI + "/static/" + str(sourceNamespace) + "/" + str(setNamespace) + "/" + str(batchTag) + "/manifest"
        urlCheck = Utils.checkURI(url)
        if not urlCheck:
            return False
        ids = []
        contents = Utils.getContent(url)
        lines = contents.split("\n")
        for line in lines:
            parts = line.split('><')
            resourceID = parts[-1]
            resourceID = resourceID.replace('/resource/','')
            resourceID = resourceID.replace('>','')
            ids.append(resourceID)
        return ids
        
    def deleteCapability(self,capURL,sourceNamespace,setNamespace):
        pass

    def getCapabilities(self,**kwargs):
        pass

    def what(self):
        print("This is a RSRestClient.")

