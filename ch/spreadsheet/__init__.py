import openpyxl
class TradingBook():
    _wb = None
    def __init__(self, configuration=None, session=None):
        self._wb = openpyxl.load_workbook(filename=configuration.getSessionXLSFile(session=session))
        #print(self._wb['#2 Oct 27']['C33'].value)
    