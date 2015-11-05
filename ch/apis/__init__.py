import requests
from ch import logger

class Response():
    _responseObj = None
    def __init__(self, responseObj=None, arguments=None):
        self._responseObj = responseObj
        self.errorCheck()
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
    
    def get(self, url, useCache=False, arguments=None, **kwargs):
        #Get provided headers (if any)
        headers = kwargs['headers'] if 'headers' in kwargs else { }
        #Ensure stripped and lowercase headers
        headers = dict((k.strip().lower(), v) for k, v in headers.items())
        #Assign no-cache if useCache is false
        if not useCache and 'cache-control' not in headers:
            headers['cache-control'] = 'no-cache'
        #Assign headers to be passed in, may be empty
        kwargs['headers'] = headers
        #Invoke request
        response = requests.get(url=url, **kwargs)
        #Provide response to response handler object
        ret = self._responseHandler(arguments=arguments, responseObj=response)
        if self._log.isDebugEnabled():
            self._log.debug("get[%s %s %s] -> [%s]" % (url, arguments, kwargs, str(ret)))
        return ret