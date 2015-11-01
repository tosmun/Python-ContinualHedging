from ch import config, logger

class Daemon(object):

    _log = None
    _configuration = None
    def __init__(self, configFilePath):
        if configFilePath is None:
            raise Exception("configFilePath is required")
        # Read configuration
        self._configuration = config.Configuration(path=configFilePath)
        # Grab a logger
        self._log = logger.Log(self._configuration, self.__class__.__name__)
        if self._log.isDebugEnabled():
            self._log.debug("%s initialized" % self.__class__.__name__)
    
    def run(self):
        #TODO
        from ch.apis import stockprice
        print(stockprice.StockPriceRequests(self._configuration).getQuote("T"))