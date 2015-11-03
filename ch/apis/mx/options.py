from ch.apis import Requests, Response

class MXOptionsResponse(Response):
    _json = None
    def __init__(self, requests, responseObj):
        super(MXOptionsResponse, self).__init__(requests, responseObj)
        #TODO parse HTML

class MXOptionsRequests(Requests):
    _api_url = None
    def __init__(self, configuration, responseHandler=MXOptionsResponse):
        super(MXOptionsRequests, self).__init__(
                configuration=configuration,
                responseHandler=responseHandler)
        self._api_url = configuration.getMxApiOptionsUrl()

    def getOption(self, symbol, instrument):
        data = { }
        data['symbol'] = symbol
        data['instrument'] = instrument
        return super(MXOptionsRequests, self).get(url=self._api_url, params=data)