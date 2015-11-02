import time
from ch import config, logger
from ch.apis import stockprice

class Daemon(object):

    _log = None
    _configuration = None
    _spr = None
    def __init__(self, configFilePath):
        if configFilePath is None:
            raise Exception("configFilePath is required")
        # Read configuration
        self._configuration = config.Configuration(path=configFilePath)
        # Grab a logger
        self._log = logger.Log(self._configuration, self.__class__.__name__)
        # Intialize api(s)
        self._spr = stockprice.StockPriceRequests(self._configuration)
        if self._log.isDebugEnabled():
            self._log.debug("%s initialized" % self.__class__.__name__)
    
    def run(self):
        intervalSec = self._configuration.getIntervalMin() * 60
        sessions = self._configuration.getSessions()
        while(True):
            for session in sessions:
                self._executeSessionInterval(session=session)
            time.sleep(intervalSec)
            
    def _executeSessionInterval(self, session):
        try:
            symbol = self._configuration.getSessionSymbol(session=session)
            exchange = self._configuration.getSessionExchange(session=session)
            ltp = self._spr.getQuote(symbol=symbol, exchange=exchange).getLastTradePrice()
            self._log.info("[%s] [%s]%s: %f" % (session, exchange, symbol, ltp))
            #TODO
        except Exception as e:
            self._log.exception("[%s] Failed to execute session interval" % session, exc_info=e)