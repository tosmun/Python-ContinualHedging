from ch.apis import Requests, Response

class YQLResponse(Response):
    _json = None
    def __init__(self, requests, responseObj):
        super(YQLResponse, self).__init__(requests, responseObj)
        self._json = super(YQLResponse, self).getContentAsJson()['query']
    def getResults(self):
        return self._json['results']

class YQLRequests(Requests):
    _RESPONSE_FORMAT = 'json' # The only format we accept
    #https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quote%20where%20symbol%20%3D%20%22T.TO%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=
    _api_url = None
    _api_env = None
    def __init__(self, configuration, responseHandler=YQLResponse):
        super(YQLRequests, self).__init__(
                configuration=configuration,
                responseHandler=responseHandler)
        self._api_url = configuration.getYqlApiUrl()
        self._api_env = configuration.getYqlApiEnv()
    
    def query(self, yql):
        data = { }
        data['q'] = yql
        data['format'] = self._RESPONSE_FORMAT
        data['env'] = self._api_env
        return super(YQLRequests, self).get(self._api_url, params=data)
