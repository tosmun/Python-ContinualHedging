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
            raise Exception('Failed to invoke %s (%d): %s' %(self._requests._NAME, self.getStatusCode(), self.getContentAsText()))

class Requests():
    _name = None
    _responseHandler = None
    _log = None
    def __init__(self, configuration, name=None, responseHandler=Response):
        self._name = name
        self._responseHandler = responseHandler
        # Grab a logger
        self._log = logger.Log(configuration, self._name)
        if self._log.isDebugEnabled():
            self._log.debug("%s initialized" % self._name)
    
    def get(self, url, **kwargs):
        response = requests.get(url=url, **kwargs)
        ret = self._responseHandler(self, response)
        ret.errorCheck()
        return ret