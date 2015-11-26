import os, csv, time, shutil, math
from distutils.command.config import config
from collections import deque

class DeltaHedge():
    _config = None
    _session = None
    _instruments = None
    _interestRate = None
    _fileName = None
    _filePath = None
    _bckFilePath = None
    _headers = None
    #Headers
    _timeH = None
    _stockPriceH = None
    _implVolH = None
    _elapsedTimeH = None
    _deltaH = None
    _sharesH = None
    #Format
    _timeFormat = None
    
    def __init__(self, config, session):
        self._config = config
        self._session = session
        self._instruments = self._config.getSessionDHInstruments(session=session)
        self._interestRate = self._config.getSessionInterestRate(session=session)
        self._fileName = self._config.getSessionDHFileFormat(session=session) % self._instruments
        self._filePath = os.path.join(self._config.getSessionDir(session=session), self._fileName)
        self._bckFilePath = "%s.bck" % self._filePath
        self._headers = self._config.getSessionDHFileHeaders(session=session)
        self._timeH = self._config.getSessionDHHTime(session=session)
        self._stockPriceH = self._config.getSessionDHHStockPrice(session=self._session)
        self._implVolH = self._config.getSessionDHHImplVol(session=self._session)
        self._elapsedTimeH = self._config.getSessionDHHElapsedTime(session=self._session)
        self._deltaH = self._config.getSessionDHHDelta(session=self._session)
        self._sharesH = self._config.getSessionDHHShares(session=self._session)
        self._timeFormat = self._config.getSessionDHTimeFormat(session=session)

    def _begin(self):
        #If it does not exist, nothing to back up
        if not os.path.isfile(self._filePath):
            return
        shutil.copy(self._filePath, self._bckFilePath)
    def _rollback(self):
        if os.path.isfile(self._bckFilePath):
            shutil.copy(self._bckFilePath, self._filePath)
    def _commit(self):
        if os.path.isfile(self._bckFilePath):
            os.remove(self._bckFilePath)
            
    def doHedge(self, spr, oprs):
        newData = _DeltaHedgeData(parent=self, spr=spr, oprs=oprs)
        #Begin write process
        self._begin()
        try:
            if not os.path.isfile(self._filePath):
                with open(self._filePath, 'w') as fp:
                    writer = csv.DictWriter(f=fp, delimiter=',', fieldnames=self._headers)
                    writer.writeheader()
            with open(self._filePath, 'a') as fp:
                writer = csv.DictWriter(f=fp, delimiter=',', fieldnames=self._headers)
                writer.writerow(newData.toDict())
            self._commit()
        except Exception as e:
            self._rollback()    
            raise e

class _DeltaHedgeData():
    _parent = None
    _stockPrice = None
    _impliedVol = None
    _timeStampSec = None
    _elapsedTimeYears = None
    _delta = -1
    _shares = -1
    def __init__(self, parent, spr, oprs):
        self._parent = parent
        self._timeStampSec = int(time.time())
        self._stockPrice = spr.getLastTradePrice()
        ourOprs = { }
        for instrument in oprs:
            #Only instruments that do not belong to us
            if instrument in parent._instruments:
                ourOprs[instrument] = oprs[instrument]
        #TODO support more some day
        if len(ourOprs) != 1:
            raise Exception("Supporting one and only one instrument for now")
        opr = next(iter(oprs.values()))
        option = opr.getOption()
        self._impliedVol = option.getImpliedVolatility()
        #TODO
        self._elapsedTimeYears = (int(self._parent._config.getHardcodedExpTime(session=self._parent._session)) - self._timeStampSec) / (60 * 60 * 24 * 365)
        
        #d2
        #TODO 42.49
        d2 = (
              math.log(self._stockPrice / 42.49) + 
                (((self._parent._interestRate - (self._impliedVol * self._impliedVol)) / 2) * self._elapsedTimeYears)
            ) / (self._impliedVol * math.sqrt(self._elapsedTimeYears))
        print(d2)
        #delta
        self._delta = -1 * math.exp(-1 * self._parent._interestRate * self._elapsedTimeYears) * (math.exp(-1 * d2*d2 / 2) / math.sqrt(2 * math.pi)) / (self._impliedVol * self._stockPrice * math.sqrt(self._elapsedTimeYears))
        self._delta *= -232000
        #TODO -232000
        self._shares = -1 * round(self._delta)
        
        
    def toDict(self):
        ret = { }
        ret[self._parent._timeH] = time.strftime(self._parent._timeFormat, time.localtime(self._timeStampSec))
        ret[self._parent._stockPriceH] = "%.2f" % self._stockPrice
        ret[self._parent._implVolH] = "%.2f" % self._impliedVol
        ret[self._parent._elapsedTimeH] = "%.5f" % self._elapsedTimeYears
        ret[self._parent._deltaH] = "%.5f" % self._delta
        ret[self._parent._sharesH] = "%d" % self._shares
        return ret;
    def __str__(self):
        return "_DeltaHedgeData: timeStampSec->%s, stockPrice->%s, impliedVol->%s, deltaHedge->%s, shares->%s" % (
            self._timeStampSec, self._stockPrice, self._impliedVol, self._deltaHedge, self._shares)