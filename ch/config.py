import os.path, configparser

class Configuration(configparser.RawConfigParser):
    _MAIN = 'Main'
    _LOGGING = 'Logging'
    _STOCK_PRICE = 'StockPrice'
    _STOCK_OPTIONS = 'StockOptions'
    def __init__(self, path=None):
        super(Configuration, self).__init__(strict=False)
        # If file path was provided, read it
        if path is not None:
            # Expand path
            path = os.path.expanduser(path)
            # Ensure exists
            if not os.path.exists(path):
                raise IOError('Configuration file "%s" does not exist' % path)
            # Read the ch_config file
            with open(path, 'r') as configFile:
                self.read_file(configFile)
                
    def getLogFilePath(self):
        return os.path.expanduser(self.get(self._LOGGING, 'logFile'))
    def getLogLevel(self):
        return self.get(self._LOGGING, 'logLevel')
    def getStockPriceSymbol(self):
        return self.get(self._STOCK_PRICE, 'symbol')
    def getStockPriceApiUrl(self):
        return self.get(self._STOCK_PRICE, 'api_url')
    def getStockPriceApiQueryFormat(self):
        return self.get(self._STOCK_PRICE, 'api_query_format')
    def getStockPriceApiFormat(self):
        return self.get(self._STOCK_PRICE, 'api_format')
    def getStockPriceApiEnv(self):
        return self.get(self._STOCK_PRICE, 'api_env')
    