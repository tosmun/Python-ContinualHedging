import requests
from ch import logger

class Response():
    _requests = None
    _responseObj = None
    def __init__(self, requests, responseObj):
        self._requests = requests
        self._responseObj = responseObj
    def getStatusCode(self):
        return self._responseObj.status_code
    def getContentAsJson(self):
        return self._responseObj.json()
    def getContentAsText(self):
        return self._responseObj.text
    def successful(self):
        return self.getStatusCode() == 200
    def errorCheck(self):
        if not self.successful():
            raise Exception('ERROR in %s (%d): %s' 
                            %(self.__class__.__name__, self.getStatusCode(), 
                              self.getContentAsText()))
    def __str__(self):
        return "%s (%d): %s" %(self.__class__.__name__, 
                               self.getStatusCode(), self.getContentAsText())
class Requests():
    _responseHandler = None
    _log = None
    def __init__(self, configuration, responseHandler=Response):
        self._responseHandler = responseHandler
        # Grab a logger
        self._log = logger.Log(configuration, self.__class__.__name__)
        if self._log.isDebugEnabled():
            self._log.debug("%s initialized" % self.__class__.__name__)
    
    def get(self, url, **kwargs):
        response = requests.get(url=url, **kwargs)
        ret = self._responseHandler(self, response)
        if self._log.isDebugEnabled():
            self._log.debug("get[%s %s] -> [%s]" % (url, kwargs, str(ret)))
        ret.errorCheck()
        return ret