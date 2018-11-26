import sys
import json
import re
import urllib.request
import requests
from requests.auth import HTTPBasicAuth

from gleanomatic.RSLoader import RSLoader,RSLoaderError
import gleanomatic.Utils as Utils


#load urls as an array from a given URL
class ListLoader(RSLoader):
    
    ListSource = None
    
    def __init__(self,sourceNamespace,setNamespace,opts):
        super().__init__(sourceNamespace,setNamespace,opts)
        self.logger.info("initializing ListLoader")
        try:
            Utils.validateRequired(opts,['ListSource'])
        except ValueError as e:
            raise RSLoaderError("Missing required parameter.",e,self.logger)
        try:
            Utils.checkURI(str(self.ListSource))
        except Exception as e:
            raise RSLoaderError("ListSource url did not validate. ", e,self.logger)
        return None
  
    def run(self):
        try:
            response = Utils.getResponse(self.ListSource)
        except Exception as e:
            raise RSLoaderError("Could not load URLs from listSource. Error: " + str(e),None,self.logger)
        records = Utils.getJSONFromResponse(response)
        self.addBatch(records)
           
           
if __name__ == "__main__":
    pass
