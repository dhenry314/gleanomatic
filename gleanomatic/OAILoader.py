import sys
from RSLoader import RSLoader
import Utils
import urllib.request
import requests
from requests.auth import HTTPBasicAuth
import json
from xmljson import badgerfish as bf
from lxml import html
from lxml import etree


class OAILoader(RSLoader):
    
    OAISource = None
    OAIMetaDataPrefix = None
    setNamespace = None
    OAIset = None
    staticOAI = False
    
    def __init__(self,sourceNamespace,setNamespace,opts):
        Utils.validateRequired(opts,['OAISource','OAIMetaDataPrefix'])
        try:
            super().__init__(sourceNamespace,setNamespace,opts)
        except Exception as e:
            raise Exception("Could not start RSLoader. " + str(e))
        try:
            Utils.checkURI(str(self.OAISource) + "?verb=Identify")
        except Exception as e:
            raise ValueError("OAISource url did not validate. " + str(e))
        return None
  
    def run(self):
        if self.staticOAI:
            self.pullStaticOAI(self.OAISource)
        else:
            self.pullDynamicOAI()
            
    def pullStaticOAI(self,uri):
        data = getAsJSON(uri)
        records = data['records']['record']
        #TODO - iterate over static records

    def getResumptionToken(self,remainder):
        #DEBUG
        print(remainder)
        exit()
        rToken = result['oai:resumptionToken']
        if isinstance(rToken, dict):
            return False
        if isinstance(rToken, str):
            return rToken
        rToken = rToken.decode('utf-8')
        if rToken.find("</"):
            tParts = rToken.split("</")
            tParts.pop()
            uglyJunk = tParts.pop()
            uParts = uglyJunk.split(">")
            rToken = uParts.pop()
        return rToken


    def pullDynamicOAI(self):
        url = str(self.OAISource) + "?verb=ListIdentifiers&metadataPrefix=" + str(self.OAIMetaDataPrefix)
        if self.OAIset:
            url = url + "&set=" + str(self.OAIset)
        while url:
            data = Utils.getContent(url)
            rawIDs = data.decode('UTF-8').split('<identifier>')
            #first item is the header
            del rawIDs[0]
            records = []
            for rawID in rawIDs:
                parts = rawID.split('</identifier>')
                records.append(parts[0])
                remainder = parts[1]
            for identifier in records:
                try:
                    resourceURL = str(self.OAISource) + "?identifier=" + str(identifier)
                    self.addResource(resourceURL)
                except Exception as e:
                    #TODO should be logged
                    print("Could not add resource. " + str(e))
            rToken = self.getResumptionToken(remainder)
            if not rToken:
                return True
            url = str(uri) + "?verb=ListIdentifiers"
            url = str(url) + "&resumptionToken=" + str(rToken)
            ids = dataLD['oai:OAI-PMH']['oai:ListIdentifiers']['oai:header']
            


    def getAsJSON(self,url):
        try:
            with urllib.request.urlopen(url) as response:
                content = response.read()
        except:
            raise ValueError("Could not load OAI request: " + str(url))
        result = bf.data(etree.fromstring(content))
        return result

if __name__ == "__main__":
    opts = {}
    opts['OAISource'] = 'https://fraser.stlouisfed.org/oai'
    opts['OAIMetaDataPrefix'] = 'mods'

    try:
        ol = OAILoader('frbstl','fraser',opts)
        ol.run()
    except:
        e = sys.exc_info()[1]
        print(str(e))
    print("main was found!")
    exit()
