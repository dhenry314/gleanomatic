import sys
import json
import re
import urllib.request
import requests
from requests.auth import HTTPBasicAuth

from gleanomatic.RSLoader import RSLoader,RSLoaderError
import gleanomatic.Utils as Utils


class RESTLoader(RSLoader):
    
    offsetVar = 'offset'
    countVar = 'count'
    recordType = 'list'
    defaultOffset = 0
    defaultCount = 1000
    
    def __init__(self,sourceNamespace,setNamespace,opts):
        super().__init__(sourceNamespace,setNamespace,opts)
        self.logger.info("initializing RESTLoader")
        try:
            Utils.validateRequired(opts,['RESTSource'])
        except ValueError as e:
            raise RSLoaderError("Missing required parameter.",e,self.logger)
        try:
            Utils.checkURI(str(self.RESTSource))
        except Exception as e:
            raise RSLoaderError("RESTSource url did not validate. ", e,self.logger)
        return None
  
    def run(self):
        offset = self.defaultOffset
        count = self.defaultCount
        url = self.getNextURL()
        while url:
            self.logger.info("Pulling REST records from "  + str(url))
            try:
                data = Utils.getContent(url)
            except Exception as e:
                self.logger.warning("Could not get content from " + str(url) + " ERROR: " + str(e))
                continue
            if len(data) == 0:
                url = None
            if self.recordType == 'list':
                records = []
                for uri in data:
                    records.append(uri)
            else:
                records = self.getRecords(url)
            self.addBatch(records)
            offset = offset + count
            url = self.getNextURL(offset,count)

    # may be overridden in subclass
    def getNextURL(offset=None,count=None):
        baseURL = str(self.RESTSource)
        if not offset:
            offset = self.defaultOffset
        if not count:
            count = self.defaultCount
        url = str(baseURL) + "?" + str(self.offsetVar) + "=" + str(offset) + "&" + str(self.countVar) + "=" + str(count)
        return url

    # to be overridden in subclass
    def getRecords():
        return []


if __name__ == "__main__":
    pass
