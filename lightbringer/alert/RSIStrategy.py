from Strategy import Strategy
class RSIStrategy(Strategy):
    def __init__(self, avTechIndicatorObj):
        Strategy.__init__(self, avTechIndicatorObj)
        
    def verify(self,symbol, interval='daily'):
        rsi, meta_data = self.avTechIndicatorObj.get_rsi(symbol=symbol, interval = interval)
        if rsi['RSI'][-1] < 50:
            return True
        else:
            return False
        