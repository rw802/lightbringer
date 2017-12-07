from Strategy import Strategy
class BBandStrategy(Strategy):
    def __init__(self, avTechIndicatorObj):
        Strategy.__init__(self, avTechIndicatorObj)
        
    #sample: low values; begin with earliest data and end with latest data 
    def verify(self, sample, length, symbol, interval = 'daily'):
        bb, meta_data = self.avTechIndicatorObj.get_bbands(symbol=symbol, interval=interval)
        for i in range(0,length):
            if sample[-1-i] < bb['Real Lower Band'][-1-i]:
                return True 
        
        return False
        