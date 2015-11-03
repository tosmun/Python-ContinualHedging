from ch.apis.yql import YQLRequests, YQLResponse

class StockPriceResponse(YQLResponse):
    _MAPPING = {
        'LastTradePriceOnly': '_lastTradePriceOnly'
    }
    def __init__(self, requests, responseObj):
        super(StockPriceResponse, self).__init__(requests, responseObj)
        quote = self.getResults()['quote']
        for key in quote:
            if key in self._MAPPING:
                setattr(self, self._MAPPING[key], quote[key])
    def getLastTradePrice(self):
        return float(self._lastTradePriceOnly)
    
    def __str__(self):
        mappingStr = ""
        for mappingItem in self._MAPPING.items():
            attrName = mappingItem[1]
            mappingStr = "%s [%s->%s]" % (mappingStr, attrName, getattr(self, attrName))
        return "%s (%d): %s" %(self.__class__.__name__, 
                               self.getStatusCode(), mappingStr)
        
class StockPriceRequests(YQLRequests):
    _query_format = None
    def __init__(self, configuration, responseHandler=StockPriceResponse):
        super(StockPriceRequests, self).__init__(
                configuration=configuration,
                responseHandler=responseHandler)
        self._query_format = configuration.getYqlApiQuoteQueryFormat()
    
    def getQuote(self, symbol, exchange):
        yql = self._query_format.format(symbol, exchange)
        return super(StockPriceRequests, self).query(yql=yql)
