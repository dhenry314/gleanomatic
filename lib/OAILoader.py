import sys
from RSLoader import RSLoader
import urllib.request
import requests
from requests.auth import HTTPBasicAuth
import json
from xmljson import badgerfish as bf
from lxml import html
from lxml import etree

class OAILoader(RSLoader):

    def run(self):
        if self.static:
            records = self.pullStaticOAI(self.OAIUrl)

    def pullStaticOAI(uri):
        data = getAsJSON(uri)
        records = data['records']['record']
        return records

    def getResumptionToken(result):
        if 'oai:resumptionToken' not in result:
            return False
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


    def pullDynamicOAI(uri, feedID, mdPrefix, setID=None):
        url = str(uri) + "?verb=ListIdentifiers&metadataPrefix=" + str(mdPrefix)
        if setID:
            url = url + "&set=" + str(setID)
        while url:
            print(url)
            data = getAsJSON(url)
            dataLD = jsonld(data)
            if 'oai:OAI-PMH' not in dataLD:
                print("Something went wrong.  No OAI-PMH node found.")
                exit()
            if 'oai:error' in dataLD['oai:OAI-PMH']:
                print(dataLD['oai:OAI-PMH']['oai:error'])
                exit()
            if 'oai:ListIdentifiers' not in dataLD['oai:OAI-PMH']:
                print("Something went wrong.  No ListIdentifiers node found!")
                exit()
            rToken = getResumptionToken(dataLD['oai:OAI-PMH']['oai:ListIdentifiers'])
            if not rToken:
                return True
            url = str(uri) + "?verb=ListIdentifiers"
            url = str(url) + "&resumptionToken=" + str(rToken)
            ids = dataLD['oai:OAI-PMH']['oai:ListIdentifiers']['oai:header']
            for record in ids:
                identifier = record['oai:identifier']
                IDresult = addIdentifier(identifier,feedID)
                if not IDresult:
                    print("Could not add identifier for " . identifier)
                print("Added " + identifier)


    def getAsJSON(url):
        try:
            with urllib.request.urlopen(url) as response:
                content = response.read()
        except:
            print ('An error occurred retrieving JSON!')
            return False
        try:
            result = bf.data(etree.fromstring(content))
        except ValueError:
            print("Could not parse XML. " + str(myResponse))
            exit()
        return result

if __name__ == "__main__":
    print("main was found!")
    exit()
