from ch.apis.yql import YQLRequests, YQLResponse

class StockPriceResponse(YQLResponse):
    _quote = None
    def __init__(self, requests, responseObj):
        super(StockPriceResponse, self).__init__(requests, responseObj)
        self._quote = super(StockPriceResponse, self).getResults()['quote']
    def getLastTradePrice(self):
        return self._quote['LastTradePriceOnly']
    
class StockPriceRequests(YQLRequests):
    _query_format = None
    def __init__(self, configuration, responseHandler=StockPriceResponse):
        super(StockPriceRequests, self).__init__(
                configuration=configuration,
                responseHandler=responseHandler)
        self._query_format = configuration.getYqlApiQuoteQueryFormat()
    
    def getQuote(self, symbol):
        yql = self._query_format.format(symbol)
        return super(StockPriceRequests, self).query(yql=yql)
