from gleanomatic.configure import appConfig
from gleanomatic.RSReader import RSReader
import gleanomatic.Utils as Utils
from gleanomatic.GleanomaticErrors import GleanomaticError,PostDataException,BadResourceURL, RSPathException, TargetURIException, AddDumpException, AddCapabilityException
import gleanomatic.gleanomaticLogger as gl

class RESTPublisher():
    
    reader = None
    logger = None
    posttype = 'params'
    
    def __init__(self,sourceNamespace,setNamespace,opts,mode='latest'):
        for key, value in opts.items():
            setattr(self, key, value)
        Utils.validateRequired(opts,['targetURL'])
        self.batchTag = Utils.getCurrentBatchTimestamp()
        self.logger = gl.gleanomaticLogger(sourceNamespace,setNamespace,self.batchTag)
        self.logger.info("Initializing RESTPublisher")
        self.reader = RSReader(sourceNamespace,setNamespace,{"batchTag":self.batchTag},mode)
  
    def run(self):
        try:
            self.reader.loadIDs()
        except Exception as e:
            raise GleanomaticError("Could not load IDs from reader.",e,self.logger) 
        self.logger.info("Loaded " + str(len(self.reader.resourceIDs)) + " resourceIDs into reader.")
        offset = 0
        while len(self.reader.resourceIDs) > offset:
            self.logger.info("Offset: " + str(offset))
            #batch by 1000
            try:
                batchIDs = self.reader.resourceIDs[offset:offset+1000]
            except KeyError as e:
                break;
            # get record, prepare the record, and post the record
            for resID in batchIDs:
                record = self.reader.getResourceContent(resID)
                record = self.prepareRecord(record,resID)
                result = self.publishRecord(record)
                internalResult = self.handleResponse(result)
                if not internalResult:
                    raise GleanomaticError("Could not handle RESTPublisher response.",None)
            offset = offset + 1000
        return True

    # override in subclass
    def prepareRecord(self,record,resID):
        return record

    # override in subclass as needed
    def handleResponse(self,response):
        return True

    def publishRecord(self,record):
        result = Utils.postREST(self.targetURL,record,'params',self.auth)
        return result
   
if __name__ == "__main__":
    pass
