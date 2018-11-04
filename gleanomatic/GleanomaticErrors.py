
class GleanomaticError(Exception):

    def __init__(self,msg,error,logger=None):
        message  = str(msg) + " " + str(error)
        if logger:
            logger.error(message)
        super().__init__(message)

class URIException(GleanomaticError):
    pass

class PostDataException(GleanomaticError):
    pass

class RSPathException(GleanomaticError):
    pass

class TargetURIException(URIException):
    pass
        
class BadResourceURL(URIException):
    pass
 
class AddResourceError(GleanomaticError):
    pass
    
class AddDumpException(GleanomaticError):
    pass

class AddCapabilityException(GleanomaticError):
    pass

