import os.path, configparser

class Configuration(configparser.RawConfigParser):
    _MAIN = 'Main'
    _LOGGING = 'Logging'
    _YQL_API = 'YQL_API'
    _YQL_API_QUOTES = 'YQL_API_Quotes'
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
    #LOGGING          
    def getLogFilePath(self):
        return os.path.expanduser(self.get(self._LOGGING, 'logFile'))
    def getLogLevel(self):
        return self.get(self._LOGGING, 'logLevel')
    #YQL_API
    def getYqlApiUrl(self):
        return self.get(self._YQL_API, 'url')
    def getYqlApiEnv(self):
        return self.get(self._YQL_API, 'env')
    #YQL_API_QUOTES
    def getYqlApiQuoteQueryFormat(self):
        return self.get(self._YQL_API_QUOTES, 'quote_query_format')
    
    