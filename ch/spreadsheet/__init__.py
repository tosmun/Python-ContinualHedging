import openpyxl
import calendar, time, datetime, os

#from xlutils.copy import copy
class TradingSessions():
    _configuration = None
    _session = None
    _refwb = None
    _refwbpath = None
    def __init__(self, configuration, session):
        self._configuration = configuration
        self._session = session
        
        self._refwbpath = self._getLatestSessionXLSFile()
        self._refwb = openpyxl.load_workbook(filename=self._getLatestSessionXLSFile())
    
    def _getLatestSessionXLSFile(self):
        latestDir = self._getLatestSessionIntervalDir()
        relXlsFile = self._configuration.getSessionXLSFile(session=self._session)
        xlsPath = os.path.join(latestDir, relXlsFile)
        if not os.path.isfile(xlsPath):
            raise Exception('Template XLS file "%s" does not exist' % xlsPath)
        return xlsPath
    
    def _getLatestSessionIntervalDir(self):
        sessionDir = self._configuration.getSessionDir(session=self._session)
        if not os.path.isdir(sessionDir):
            raise Exception('Session directory "%s" does not exist. Create it' % sessionDir)
        latestEpoch = -1
        latestDir = None
        for x in os.listdir(sessionDir):
            #Ignore hidden files on unix
            if str(x).startswith('.'):
                continue
            xEpoch = float(x)
            if latestEpoch < xEpoch:
                latestEpoch = xEpoch
                latestDir = os.path.join(sessionDir, x)
        if latestDir is None or not os.path.isdir(latestDir):
            raise Exception('Require at least one session entry in "%s"' % sessionDir)
        return latestDir
    
    def newTradingSession(self):
        wbcopy = openpyxl.load_workbook(filename=self._refwbpath)
        return TradingSession(wb=wbcopy, config=self._configuration, session=self._session)
    
    def commitTradingSession(self, tradingSession, outputDir):
        if not os.path.isdir(outputDir):
            os.mkdir(outputDir)
        newPath = os.path.join(outputDir, self._configuration.getSessionXLSFile(session=self._session))
        tradingSession._save(filepath=newPath)
        self._refwb = tradingSession
        self._refwbpath= newPath

class TradingSession():
    _config = None
    _session = None
    _wb = None
    _sheet = None
    def __init__(self, wb, config, session):
        self._config = config
        self._session = session
        self._wb = wb
        sheetName = self._config.getSessionXLSSheetName(session=session)
        if not sheetName in self._wb.get_sheet_names():
            raise Exception('Source sheet "%s" does not exist in workbook "%s"' % (sheetName, self._wbpath))
        self._sheet = self._wb.get_sheet_by_name(sheetName)
        self._assignDates()
    def _assignDates(self):
        prevDateCell = self._config.getSessionXLSPreviousDateCell(session=self._session)
        dateCell = self._config.getSessionXLSDateCell(session=self._session)
        newDate = datetime.datetime.now()
        prevDate = self._sheet[dateCell].value
        self._sheet[dateCell].value = newDate
        self._sheet[prevDateCell].value = prevDate
    def applyStockPrice(self, stockprice):
        cell = self._config.getSessionXLSUnitPriceCell(session=self._session)
        self._sheet[cell] = stockprice.getLastTradePrice()
        return 
    def applyOption(self, option):
        instrument = option.getInstrument()
        optionObj = option.getOption()
        #Strike price
        strikeCell = self._config.getSessionInstrumentXLSStrikeCell(session=self._session, instrument=instrument)
        if strikeCell is not None and strikeCell.strip() != '':
            self._sheet[strikeCell].value = optionObj.getLastPrice()
        volCell = self._config.getSessionInstrumentXLSVolatilityCell(session=self._session, instrument=instrument)
        if volCell is not None and volCell.strip() != '':
            self._sheet[volCell].value = optionObj.getImpliedVolatility() / 100
        bidOptionPriceCell = self._config.getSessionInstrumentXLSBidOptionPriceCell(session=self._session, instrument=instrument)
        if bidOptionPriceCell is not None and bidOptionPriceCell.strip() != '':
            self._sheet[bidOptionPriceCell].value = optionObj.getBidPrice()
        askOptionPriceCell = self._config.getSessionInstrumentXLSAskOptionPriceCell(session=self._session, instrument=instrument)
        if askOptionPriceCell is not None and askOptionPriceCell.strip() != '':
            self._sheet[askOptionPriceCell].value = optionObj.getAskPrice()
    def _save(self, filepath):
        self._wb.save(filename=filepath)