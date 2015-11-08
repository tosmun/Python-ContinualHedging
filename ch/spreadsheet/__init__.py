import openpyxl
import calendar, time
#from xlutils.copy import copy
class TradingBook():
    _wb = None
    _sourceSheet = None
    _newSheet = None
    _configuration = None
    def __init__(self, configuration, session):
        self._configuration = configuration
        self._wb = openpyxl.load_workbook(filename=self._configuration.getSessionXLSFile(session=session))
        sourceSheetName = self._configuration.getSessionXLSSourceSheet(session=session)
        if sourceSheetName not in self._wb:
            raise Exception("Source sheet '%s' does not exist" % sourceSheetName)
        self._sourceSheet = self._wb[sourceSheetName]
        #COPY HERE
        self._newSheet.setName(self._wb.copycalendar.timegm(time.gmtime()))
    
    def applyUnitPrice(self, stockprice):
        #TODO
        return 
    def applyOption(self, option):
        instrument = option.getInstrument()
        