from gleanomatic.configure import appConfig
from gleanomatic.RSReader import RSReader
from gleanomatic.RSLoader import RSLoader
import gleanomatic.Utils as Utils
from gleanomatic.GleanomaticErrors import GleanomaticError,PostDataException,BadResourceURL, RSPathException, TargetURIException, AddDumpException, AddCapabilityException


class Transformer():
    
    transformURI = None
    transformName = None
    targetSet = None
    targetSourceNS = None
    targetSetNS = None
    reader = None
    loader = None
    logger = None
    
    def __init__(self,sourceNamespace,setNamespace,opts,mode='latest'):
        self.transformURI = appConfig.transformURI
        for key, value in opts.items():
            setattr(self, key, value)
        Utils.validateRequired(opts,['transformName','targetSet'])
        #parse target namespaces out of targetSet
        parts = self.targetSet.split('/')
        self.targetSourceNS = parts[0]
        self.targetSetNS = parts[1]
        self.loader = RSLoader(self.targetSourceNS,self.targetSetNS)
        self.reader = RSReader(sourceNamespace,setNamespace,{"batchTag":self.loader.batchTag},mode)
        self.logger = self.loader.logger
        self.logger.info("initializing Transformer")
  
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
            uris = map(lambda resID: str(self.transformURI) + str(self.transformName) + "/" + resID,batchIDs)
            self.loader.addBatch(uris)
            offset = offset + 1000
        self.logger.info("Requesting data dump.")
        self.loader.makeDump()
        return True
   
if __name__ == "__main__":
    pass
