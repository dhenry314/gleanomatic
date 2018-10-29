import sys
import json
import re
import urllib.request
import requests
from requests.auth import HTTPBasicAuth

from gleanomatic.RSLoader import RSLoader
import gleanomatic.Utils as Utils


class OAILoader(RSLoader):
    
    OAISource = None
    OAIMetaDataPrefix = None
    setNamespace = None
    OAISets = None
    staticOAI = False
    
    def __init__(self,sourceNamespace,setNamespace,opts):
        try:
            super().__init__(sourceNamespace,setNamespace,opts)
        except Exception as e:
            raise Exception("Could not start RSLoader. " + str(e))       
        self.logger.info("initializing OAILoader")
        Utils.validateRequired(opts,['OAISource','OAIMetaDataPrefix'])
        try:
            Utils.checkURI(str(self.OAISource) + "?verb=Identify")
        except Exception as e:
            self.logger.critical(self.msg("OAISource url did not validate. " + str(e)))
            raise ValueError("OAISource url did not validate. " + str(e))
        return None
  
    def run(self):
        if self.staticOAI:
            self.pullStaticOAI(self.OAISource)
        else:
            self.pullDynamicOAI()
        self.makeDump()
        return True
            
    def pullStaticOAI(self,uri):
        self.logger.info("Pulling static OAI from " + str(uri))
        data = getAsJSON(uri)
        records = data['records']['record']
        #TODO - iterate over static records

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
        if self.OAISets:
            for setSpec in self.OAISets:
                url = str(self.OAISource) + "?verb=ListIdentifiers&metadataPrefix=" + str(self.OAIMetaDataPrefix) + "&set=" + str(setSpec)
                self.pullDynamicOAIByURL(url)
        else:
            url = str(self.OAISource) + "?verb=ListIdentifiers&metadataPrefix=" + str(self.OAIMetaDataPrefix)
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
                self.logger.critical("Could not pull OAI records. Error: " + str(OAIerror))
                raise ValueError("Could not pull OAI records. ERROR:  " + str(OAIerror))
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
        except:
            raise ValueError("Could not load OAI request: " + str(url))
        result = bf.data(etree.fromstring(content))
        return result

if __name__ == "__main__":
    pass
