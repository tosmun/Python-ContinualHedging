import openpyxl
import calendar, time, datetime

#from xlutils.copy import copy
class TradingBook():
    _wb = None
    _sourceSheet = None
    _configuration = None
    _session = None
    def __init__(self, configuration, session):
        self._configuration = configuration
        self._session = session
        
        self._wb = openpyxl.load_workbook(filename=self._configuration.getSessionXLSFile(session=self._session))
        sourceSheetName = self._configuration.getSessionXLSSourceSheet(session=self._session)
        if sourceSheetName is None or '' == sourceSheetName:
            self._sourceSheet = self._wb.get_sheet_by_name(self._wb.get_sheet_names()[-1])
        elif sourceSheetName not in self._wb.get_sheet_names():
            raise Exception("Source sheet '%s' does not exist" % sourceSheetName)
        else:
            self._sourceSheet = self._wb.get_sheet_by_name(name=sourceSheetName)
        #DELETE ME
        self.save()
    
    def newSheet(self):
        from openpyxl.worksheet import Worksheet
        #TODO
        title = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        new_sheet = Worksheet(parent=self._wb, title=title)
        for row, columnCell in enumerate(self._sourceSheet.rows):
            row = row + 1
            for column, cell in enumerate(columnCell):
                column = column + 1
                #if cell.value is not None:
                new_sheet.cell(row=row, column=column, value=cell.value)
                new_sheet._get_cell(row=row, column=column)._style  = self._sourceSheet._get_cell(row=row, column=column)._style
        self._sourceSheet = new_sheet
        return TradingBookSheet(self._wb, self._sourceSheet, self._configuration, self._session)
    
    def save(self):
        self._wb.save(filename=self._configuration.getSessionXLSFile(session=self._session))

class TradingBookSheet():
    _wb = None
    _sheet = None
    _config = None
    def __init__(self, wb, sheet, config, session):
        self._wb = wb
        self._sheet = sheet
        self._config = config
        self._session = session
    def applyStockPrice(self, stockprice):
        cell = self._config.getSessionXLSUnitPriceCell(session=self._session)
        self._sheet[cell] = stockprice.getLastTradePrice()
        return 
    def applyOption(self, option):
        instrument = option.getInstrument()
        
    def commit(self):
        self._wb._add_sheet(sheet=self._sheet)