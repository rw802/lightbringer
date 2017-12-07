from Strategy import Strategy
class MACDStrategy(Strategy):
    def __init__(self, avTechIndicatorObj):
        Strategy.__init__(self, avTechIndicatorObj)
        
    def verify(self,symbol, interval='daily', fastperiod=12, slowperiod = 26, signalperiod = 9):
        macd, meta_data = self.avTechIndicatorObj.get_macd(symbol=symbol, interval=interval, fastperiod=fastperiod, slowperiod = slowperiod, signalperiod = signalperiod)
        # if histogram > 0
        if macd['MACD_Hist'][-1] <= 0:
            return False
        
        # if macd and signal crossed recently
        for i in range(2,6):
            if macd['MACD_Hist'][-i] <= 0:
                return True
            
        return False
        