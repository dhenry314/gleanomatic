import sys
import json
from elasticsearch import Elasticsearch
import re
import urllib.request
import requests
from requests.auth import HTTPBasicAuth

from gleanomatic.RSLoader import RSLoader,RSLoaderError
import gleanomatic.Utils as Utils


class ESLoader(RSLoader):
    
    timeout = 1000
    size =1000
    keys = []
    
    def __init__(self,sourceNamespace,setNamespace,opts):
        super().__init__(sourceNamespace,setNamespace,opts)
        self.logger.info("initializing ESLoader")
        try:
            Utils.validateRequired(opts,['ESHost','ESPort','ESIndex','ESType','body'])
        except ValueError as e:
            raise RSLoaderError("Missing required parameter.",e,self.logger)
        self.es = Elasticsearch(
			[
				{
					'host': self.ESHost,
					'port': self.ESPort
				}
			],
			timeout=self.timeout
		)
        if not self.es.indices.exists(index=self.ESIndex):
            raise RSLoaderError("ES Index " + self.ESIndex + " not exist.")
        self.baseRecordURL = 'http://' + str(self.ESHost) + ':' + str(self.ESPort) + '/' + str(self.ESIndex) + '/' + str(self.ESType) + '/'
        return None
        
    def processKeys(self,hits):
        for item in hits:
            self.keys.append(item['_id'])
  
    def getKeys(self):
        data = self.es.search(
			index=self.ESIndex,
			doc_type=self.ESType,
			scroll='2m',
			size=self.size,
			body=self.body
		)

        # Get the scroll ID
        sid = data['_scroll_id']
        scroll_size = len(data['hits']['hits'])

        # Before scroll, process current batch of hits
        self.processKeys(data['hits']['hits'])

        while scroll_size > 0:
            
            data = self.es.scroll(scroll_id=sid, scroll='2m')

            # Process current batch of hits
            self.processKeys(data['hits']['hits'])

            # Update the scroll ID
            sid = data['_scroll_id']

            # Get the number of results that returned in the last scroll
            scroll_size = len(data['hits']['hits'])
  
    def run(self):
        self.getKeys()
        keyCount = len(self.keys)
        offset = 0
        count = 1000
        while offset < keyCount:
            urls = []
            endCount = offset + count
            for key in self.keys[offset:endCount]:
                url = str(self.baseRecordURL) + str(key)
                urls.append(url)
            self.addBatch(urls)
            offset = offset + count
        self.logger.info("Requesting dump file.")
        self.makeDump()
        return True
            

        

    #To be overridden in subclass
    def filterInput(self,record):
        pass

if __name__ == "__main__":
    pass
