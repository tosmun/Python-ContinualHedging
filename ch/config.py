import os.path, configparser, re

class Configuration(configparser.RawConfigParser):
    _LOGGING = 'Logging'
    _YAHOO_API = 'Yahoo API'
    _YAHOO_API_QUOTES = 'Yahoo API Quotes'
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
        return re.split(pattern='\s*,\s*', string=self.get(self._CONTINUAL_HEDGING, 'sessions'))
    def getIntervalMin(self):
        return float(self.get(self._CONTINUAL_HEDGING, 'interval_min'))
    #SESSIONS
    def getSessionSymbol(self, session):
        return self.get(session, 'symbol')
    def getSessionExchange(self, session):
        return self.get(session, 'exchange')
    def getSessionXLSFile(self, session):
        return self.get(session, 'xls_file')
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
    
    
    