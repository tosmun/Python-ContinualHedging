import calendar, time, os
from ch import config, logger
from ch.apis.yql import stockprice
from ch.apis.mx import option
from ch.csv.delta import DeltaHedge
class Daemon(object):
    _log = None
    _intervalSec = None
    _sessions = [ ]
    _configuration = None
    _spr = None
    _mxop = None
    _deltaHedges = { }
    def __init__(self, configFilePath):
        if configFilePath is None:
            raise Exception("configFilePath is required")
        # Read configuration
        self._configuration = config.Configuration(path=configFilePath)
        # Grab a logger
        self._log = logger.Log(self._configuration, self.__class__.__name__)
        # Intialize api(s)
        self._spr = stockprice.YQLStockPriceRequests(self._configuration)
        self._mxop = option.MXOptionRequests(self._configuration)
        #Config
        self._intervalSec = self._configuration.getIntervalMin() * 60
        self._sessions = self._configuration.getSessions()
        #Initialize output dir
        outputDir = self._configuration.getOutputDir()
        if os.path.isfile(outputDir):
            raise Exception('Output directory "%s" is a file' % outputDir)
        elif not os.path.exists(outputDir):
            os.mkdir(outputDir, mode=755)
        #Initialize hedges
        for session in self._sessions:
            self._deltaHedges[session] = DeltaHedge(config=self._configuration, session=session)
        if self._log.isDebugEnabled():
            self._log.debug("%s initialized" % self.__class__.__name__)
    
    def run(self):
        while(True):
            for session in self._sessions:
                self._executeSessionInterval(session=session)
            time.sleep(self._intervalSec)
            
    def _executeSessionInterval(self, session):
        try:
            # Get config values for this session
            symbol = self._configuration.getSessionSymbol(session=session)
            exchange = self._configuration.getSessionExchange(session=session)
            instruments = self._configuration.getSessionInstruments(session=session)

            # Quote
            spr = self._spr.getQuote(symbol=symbol, exchange=exchange)
            self._log.info("[%s] [%s]%s: %s" % (session, exchange, symbol, str(spr)))
            
            oprs = { }
            # Options
            for instrument in instruments:
                mxopResponse = self._mxop.getOption(instrument=instrument)
                self._log.info("[%s] [%s]: %s" % (session, instrument, str(mxopResponse)))
                oprs[instrument] = mxopResponse
            
            self._deltaHedges[session].doHedge(spr=spr, oprs=oprs)
            
        except Exception as e:
            self._log.exception("[%s] Failed to execute session interval" % session, exc_info=e)