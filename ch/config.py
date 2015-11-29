import os.path, configparser, re

class Configuration(configparser.RawConfigParser):
    _LOGGING = 'Logging'
    _YAHOO_API = 'Yahoo API'
    _YAHOO_API_QUOTES = 'Yahoo API Quotes'
    _MX_OPTIONS = 'Montreal Exchange API Options'
    _CONTINUAL_HEDGING = 'Continual Hedging'
    def __init__(self, path=None):
        super(Configuration, self).__init__(strict=False)
        if path is None:
            raise Exception("path is required")
        # If file path was provided, read it
        # Expand path
        path = os.path.expanduser(path)
        # Ensure exists
        if not os.path.exists(path):
            raise IOError('Configuration file "%s" does not exist' % path)
        # Read the ch_config file
        with open(path, 'r') as configFile:
            self.read_file(configFile)
    #CONTINUAL_HEDGING
    def getSessions(self):
        return [x for x in re.split(pattern='\s*,\s*', string=self.get(self._CONTINUAL_HEDGING, 'sessions')) if x.strip() != ""]
    def getIntervalMin(self):
        return float(self.get(self._CONTINUAL_HEDGING, 'interval_min'))
    def getOutputDir(self):
        return self.get(self._CONTINUAL_HEDGING, 'output_dir')
    #SESSIONS
    def getSessionSymbol(self, session):
        return self.get(session, 'symbol')
    def getSessionExchange(self, session):
        return self.get(session, 'exchange')
    def getSessionInterestRate(self, session):
        return float(self.get(session, 'interest_rate'))
    def getSessionInstruments(self, session):
        return self.getSessionDHInstruments(session=session)
    def getSessionDir(self, session):
        return os.path.join(self.getOutputDir(), session)
    #DELTA HEDGE
    def getSessionDHInstruments(self, session):
        return [x for x in re.split(pattern='\s*,\s*', string=self.get(session, 'dh_instruments')) if x.strip() != ""]
    def getSessionDHFileFormat(self, session):
        return self.get(session, 'dh_file_format')
    def getSessionDHVerifyOnStart(self, session):
        return self.get(session, 'dh_verify_on_start') == 'true'
    def getSessionDHFileHeaders(self, session):
        return [x for x in re.split(pattern='\s*,\s*', string=self.get(session, 'df_file_headers')) if x.strip() != ""]
    def getSessionDHHTime(self, session):
        return self.get(session, 'df_h_time')
    def getSessionDHHStockPrice(self, session):
        return self.get(session, 'df_h_stock_price')
    def getSessionDHHImplVol(self, session):
        return self.get(session, 'df_h_impl_vol')
    def getSessionDHHTimeR(self, session):
        return self.get(session, 'df_h_time_r')
    def getSessionDHHDelta(self, session):
        return self.get(session, 'df_h_delta')
    def getSessionDHHShares(self, session):
        return self.get(session, 'df_h_shares')
    def getSessionDHTimeFormat(self, session):
        return self.get(session, 'df_h_time_format')
    def getHardcodedExpTime(self, session):
        return self.get(session, 'expiration_date_sec')
    #LOGGING          
    def getLogFilePath(self):
        return os.path.expanduser(self.get(self._LOGGING, 'log_file'))
    def getLogLevel(self):
        return self.get(self._LOGGING, 'log_level')
    #YAHOO_API
    def getYqlApiUrl(self):
        return self.get(self._YAHOO_API, 'url')
    def getYqlApiEnv(self):
        return self.get(self._YAHOO_API, 'env')
    #YAHOO_API_QUOTES
    def getYqlApiQuoteQueryFormat(self):
        return self.get(self._YAHOO_API_QUOTES, 'quote_query_format')
    #MX OPTIONS
    def getMxApiOptionsUrl(self):
        return self.get(self._MX_OPTIONS, 'url')
    
    
    