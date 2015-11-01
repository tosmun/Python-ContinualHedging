from ch.apis import Requests, Response

class StockPriceResponse(Response):
    _json = None
    def __init__(self, requests, responseObj):
        super(StockPriceResponse, self).__init__(requests, responseObj)
        self._json = super(StockPriceResponse, self).getContentAsJson()['query']
    def getTimestamp(self):
        return self._json['created']
    def getLastTradePrice(self):
        return self._getQuoteData()['LastTradePriceOnly']
    def _getQuoteData(self):
        return self._getResults()['quote']
    def _getResults(self):
        return self._json['results']
class StockPriceRequests(Requests):
    #https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quote%20where%20symbol%20%3D%20%22T.TO%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=
    _api_url = None
    _yql = None
    _api_query_format = None
    _api_format = None
    _api_env = None
    def __init__(self, configuration):
        super(StockPriceRequests, self).__init__(
                configuration=configuration,
                responseHandler=StockPriceResponse)
        self._api_url = configuration.getStockPriceApiUrl()
        self._yql = str(configuration.getStockPriceApiQueryFormat()).format(configuration.getStockPriceSymbol())
        self._api_format = configuration.getStockPriceApiFormat()
        self._api_env = configuration.getStockPriceApiEnv()
    
    def get(self):
        data = { }
        data['q'] = self._yql
        data['format'] = self._api_format
        data['env'] = self._api_env
        return super(StockPriceRequests, self).get(self._api_url, params=data)
