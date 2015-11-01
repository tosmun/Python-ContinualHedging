import time
from ch import config, logger
from ch.apis import stockprice

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
        intervalSec = self._configuration.getIntervalMin() * 60
        sessions = self._configuration.getSessions()
        spr = stockprice.StockPriceRequests(self._configuration)
        while(True):
            for session in sessions:
                symbol = self._configuration.getSessionSymbol(session=session)
                exchange = self._configuration.getSessionExchange(session=session)
                ltp = spr.getQuote(symbol=symbol, exchange=exchange).getLastTradePrice()
                self._log.info("%s[%s]: %f" % (symbol, exchange, ltp))
            time.sleep(intervalSec)