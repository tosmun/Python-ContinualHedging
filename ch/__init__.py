import time
from ch import config, logger
from ch.apis.yql import stockprice
from ch.apis.mx import option

class Daemon(object):

    _log = None
    _configuration = None
    _spr = None
    _mxop = None
    def __init__(self, configFilePath):
        if configFilePath is None:
            raise Exception("configFilePath is required")
        # Read configuration
        self._configuration = config.Configuration(path=configFilePath)
        # Grab a logger
        self._log = logger.Log(self._configuration, self.__class__.__name__)
        # Intialize api(s)
        self._spr = stockprice.StockPriceRequests(self._configuration)
        self._mxop = option.MXOptionRequests(self._configuration)
        if self._log.isDebugEnabled():
            self._log.debug("%s initialized" % self.__class__.__name__)
    
    def run(self):
        intervalSec = self._configuration.getIntervalMin() * 60
        sessions = self._configuration.getSessions()
        #from ch.spreadsheet import XLSReader
        #reader = XLSReader(configuration=self._configuration, session=sessions[0])
        while(True):
            for session in sessions:
                self._executeSessionInterval(session=session)
            time.sleep(intervalSec)
            
    def _executeSessionInterval(self, session):
        try:
            # Get config values for this session
            symbol = self._configuration.getSessionSymbol(session=session)
            exchange = self._configuration.getSessionExchange(session=session)
            instrument = self._configuration.getSessionInstrument(session=session)

            # Quote
            sprResponse = self._spr.getQuote(symbol=symbol, exchange=exchange)
            
            # Option
            mxopResponse = self._mxop.getOption(instrument=instrument)
            
            self._log.info("[%s] [%s]%s: %s" % (session, exchange, symbol, str(sprResponse)))
            self._log.info("[%s] [%s]: %s" % (session, instrument, str(mxopResponse)))
            
        except Exception as e:
            self._log.exception("[%s] Failed to execute session interval" % session, exc_info=e)