from ch.apis.yql import YQLRequests, YQLResponse

class YQLStockPriceResponse(YQLResponse):
    _MAPPING = {
        'LastTradePriceOnly': '_lastTradePriceOnly'
    }
    def __init__(self, responseObj=None, arguments=None):
        super(YQLStockPriceResponse, self).__init__(responseObj=responseObj, arguments=arguments)
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
        
class YQLStockPriceRequests(YQLRequests):
    _query_format = None
    def __init__(self, configuration, responseHandler=YQLStockPriceResponse):
        super(YQLStockPriceRequests, self).__init__(
                configuration=configuration,
                responseHandler=responseHandler)
        self._query_format = configuration.getYqlApiQuoteQueryFormat()
    
    def getQuote(self, symbol, exchange):
        yql = self._query_format.format(symbol, exchange)
        return super(YQLStockPriceRequests, self).query(yql=yql)
