import re
from lxml import html
from ch.apis import Requests, Response

class MXOptionResponse(Response):
    _MAPPING = {
        'last price:': '_lastPrice',
        'net change:': '_netChange',
        'volume:': '_volume',
        'bid price:': '_bidPrice',
        'bid size:': '_bidSize',
        'open interest:': '_openInterest',
        'ask price:': '_askPrice',
        'ask size:': '_askSize',
        'implied volatility:': '_impliedVolatility'
    }
    _instrument = None
    _option = None
    def __init__(self, responseObj=None, arguments=None):
        super(MXOptionResponse, self).__init__(responseObj=responseObj, arguments=arguments)
        htmlTree = html.fromstring(self.getContentAsText())
        kwargs = { }
        for tr in htmlTree.xpath('//div[@id="quotes"]/section/section/table/tbody/tr'):
            td = tr.xpath('./td')
            #For each header in the table row
            for i, th in enumerate(tr.xpath('./th')):
                th_text = th.text.strip().lower() if th.text is not None else ''
                #If it is a mapped name
                if th_text in self._MAPPING:
                    #Throw exception if no value is present
                    if len(td) <= i:
                        raise Exception('Failed to match value for "%s" using index %d"' % (th_text, i))
                    #Assume all values are float, trim any spacing or symbols
                    #TODO fix me
                    if td[i].text == '--':
                        td[i].text = '-1'
                    kwargs[self._MAPPING[th_text]] = float(re.sub('\s*([-+]?(?:\d*[.])?\d+).*', '\g<1>', td[i].text))
        self._instrument = arguments['instrument']
        #TODO Retrieve this from the HTML? We can probably stick with hardcoding from the name
        optionType = 'CALL' if 'C' in self._instrument.upper() else 'PUT'
        kwargs['_strikePrice'] = float(re.sub('\w+\s+[0-9]+(?:C|P)([-+]?(?:\d*[.])?\d+)', '\g<1>', self._instrument))
        self._option = MXOption(optionType=optionType, **kwargs)
        
    def getInstrument(self):
        return self._instrument
    
    def getOption(self):
        return self._option
    
    def __str__(self):
        return "%s (%d): %s" %(self.__class__.__name__, 
                               self.getStatusCode(), self.getOption())

class MXOption():
    _ATTRIBUTES = [
        "_lastPrice",
        "_netChange",
        "_volume",
        "_bidPrice",
        "_bidSize",
        "_openInterest",
        "_askPrice",
        "_askSize",
        "_impliedVolatility",
        "_strikePrice",
    ]
    def __init__(self, optionType=None, **kwargs):
        self._optionType = optionType
        for attrName in kwargs:
            if attrName in self._ATTRIBUTES:
                setattr(self, attrName, kwargs[attrName])
        return
    
    def getType(self):
        return self.optionType
    def getStrikePrice(self):
        return self._strikePrice
    def getLastPrice(self):
        return self._lastPrice
    def getNetChange(self):
        return self._netChange
    def getVolume(self):
        return self._volume
    def getBidPrice(self):
        return self._bidPrice
    def getBidSize(self):
        return self._bidSize
    def getOpenInterest(self):
        return self._openInterest
    def getAskPrice(self):
        return self._askPrice
    def getAskSize(self):
        return self._askSize
    def getImpliedVolatility(self):
        return self._impliedVolatility
    
    def __str__(self):
        mappingStr = ""
        for attrName in self._ATTRIBUTES:
            mappingStr = "%s [%s->%f]" % (mappingStr, attrName, getattr(self, attrName))
        return "%s [%s] %s" %(self.__class__.__name__, self._optionType, mappingStr)
    
class MXOptionRequests(Requests):
    _api_url = None
    def __init__(self, configuration, responseHandler=MXOptionResponse):
        super(MXOptionRequests, self).__init__(
                configuration=configuration,
                responseHandler=responseHandler)
        self._api_url = configuration.getMxApiOptionsUrl()

    def getOption(self, instrument=None):
        data = { }
        data['instrument'] = instrument
        return super(MXOptionRequests, self).get(url=self._api_url, arguments={'instrument':instrument}, params=data)