import sys
import json
import re
import urllib.request
import requests
from requests.auth import HTTPBasicAuth

from gleanomatic.RSLoader import RSLoader,RSLoaderError
import gleanomatic.Utils as Utils


class OAILoader(RSLoader):
    
    OAISource = None
    OAIMetaDataPrefix = None
    setNamespace = None
    OAISets = None
    staticOAI = False
    
    def __init__(self,sourceNamespace,setNamespace,opts):
        super().__init__(sourceNamespace,setNamespace,opts)
        self.logger.info("initializing OAILoader")
        try:
            Utils.validateRequired(opts,['OAISource','OAIMetaDataPrefix'])
        except ValueError as e:
            raise RSLoaderError("Missing required parameter.",e,self.logger)
        try:
            Utils.checkURI(str(self.OAISource) + "?verb=Identify")
        except Exception as e:
            raise RSLoaderError("OAISource url did not validate. ", e,self.logger)
        return None
  
    def run(self):
        if self.staticOAI:
            self.pullStaticOAI(self.OAISource)
        else:
            self.pullDynamicOAI()
        self.logger.info("Requesting dump file.")
        self.makeDump()
        return True
            
    def pullStaticOAI(self,uri):
        self.logger.info("Pulling static OAI from " + str(uri))
        result = self.addResource(uri)

    def getResumptionToken(self,data):
        result = re.findall("<resumptionToken(.*?)</resumptionToken>", data)
        if len(result) == 0:
            return False
        if ">" in result[0]:
            parts = result[0].split(">")
            result = parts[1]
        return result
        
    def getError(self,data):
        result = re.findall("<error(.*?)</error>", data)
        if len(result) == 0:
            return False
        if ">" in result[0]:
            parts = result[0].split(">")
            result = parts[1]
        return result
        
    def pullDynamicOAI(self):
        url = str(self.OAISource) + "?verb=ListIdentifiers&metadataPrefix=" + str(self.OAIMetaDataPrefix)
        if self.OAISets:
            for setSpec in self.OAISets:
                url = url + "&set=" + str(setSpec)
                self.pullDynamicOAIByURL(url)
        else:
            self.pullDynamicOAIByURL(url)
            
    def pullDynamicOAIByURL(self,url):
        while url:
            self.logger.info("Pulling dynamic OAI from "  + str(url))
            try:
                data = Utils.getContent(url)
            except Exception as e:
                self.logger.warning("Could not get content from " + str(url) + " ERROR: " + str(e))
                continue
            OAIerror = self.getError(data)
            if OAIerror:
                raise RSLoaderError("Could not pull OAI records. OAIError: " + str(OAIerror),None,self.logger)
            rawIDs = data.split('<identifier>')
            #first item is the header
            del rawIDs[0]
            records = []
            result = None
            for rawID in rawIDs:
                parts = rawID.split('</identifier>')
                resourceURL = str(self.OAISource) + "?verb=GetRecord&metadataPrefix=" + str(self.OAIMetaDataPrefix) + "&identifier=" + str(parts[0])
                records.append(resourceURL)
            self.addBatch(records)
            rToken = self.getResumptionToken(data)
            if rToken:
                url = str(self.OAISource) + "?verb=ListIdentifiers&resumptionToken=" + str(rToken)
            else:
                url = None

    def getAsJSON(self,url):
        try:
            with urllib.request.urlopen(url) as response:
                content = response.read()
        except Exception as e:
            raise RSLoaderError("Could not load OAI request: " + str(url),e,self.logger)
        try:
            result = bf.data(etree.fromstring(content))
        except Exception as e:
            raise RSLoaderError("Could not get JSON from content: " + str(content),e,sef.logger)
        return result

if __name__ == "__main__":
    pass
