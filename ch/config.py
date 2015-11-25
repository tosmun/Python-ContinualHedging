import calendar, time, os.path, configparser, re

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
    def getSessionInstruments(self, session):
        return [x for x in re.split(pattern='\s*,\s*', string=self.get(session, 'instruments')) if x.strip() != ""]
    def getSessionXLSFile(self, session):
        return self.get(session, 'xls_file')
    def getSessionXLSDateCell(self, session):
        return self.get(session, 'xls_date_cell')
    def getSessionXLSPreviousDateCell(self, session):
        return self.get(session, 'xls_previous_date_cell')
    def getSessionXLSSheetName(self, session):
        return self.get(session, 'xls_sheet_name')
    def getSessionInstrumentXLSIDCell(self, session, instrument):
        return self.get("%s %s" % (session, instrument), 'xls_id_cell')
    def getSessionInstrumentXLSStrikeCell(self, session, instrument):
        return self.get("%s %s" % (session, instrument), 'xls_strike_cell')
    def getSessionInstrumentXLSVolatilityCell(self, session, instrument):
        return self.get("%s %s" % (session, instrument), 'xls_volatility_cell')
    def getSessionInstrumentXLSBidOptionPriceCell(self, session, instrument):
        return self.get("%s %s" % (session, instrument), 'xls_bid_option_price_cell')
    def getSessionInstrumentXLSAskOptionPriceCell(self, session, instrument):
        return self.get("%s %s" % (session, instrument), 'xls_ask_option_price_cell')
    def getSessionXLSUnitPriceCell(self, session):
        return self.get(session, 'xls_unit_price_cell')
    def getSessionDir(self, session):
        return os.path.join(self.getOutputDir(), session)
    def getNewSessionIntervalDir(self, session):
        return os.path.join(self.getSessionDir(session=session), str(calendar.timegm(time.gmtime())))
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
    
    
    