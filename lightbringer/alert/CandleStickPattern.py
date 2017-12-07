class CandleStickPattern:
    
    # first, second, third are three data samples, where third is the latest (current).
    def __init__(self, first, second, third):
        self.first = first
        self.second = second
        self.third = third
        
    def bearish(self, data):
        return (data['open'] > data['close'])
    
    def bullish(self, data):
        return (data['open'] < data['close'])
    
    def bullishEngulf(self):
        if self.bullish(self.second) or self.bearish(self.third):
            return False
        return (self.second['open'] < self.third['close']) and (self.second['close'] > self.third['open']) and (self.second['low'] > self.third['low']) and (self.second['high'] < self.third['high'])
    
    def bearishEngulf(self):
        if self.bullish(self.third) or self.bearish(self.second):
            return False
        
        return (self.second['open'] > self.third['close']) and (self.second['close'] < self.third['open']) and (self.second['low'] > self.third['low']) and (self.second['high'] < self.third['high'])
    
    def bullishPin(self):
        if self.bullish(self.second):
            return False
        
        lowhighRange = abs(self.third['high'] - self.third['low'])
        bottomValue = min(self.third['open'], self.third['close'])
        if abs(bottomValue - self.third['high']) > lowhighRange * 0.33:
            return False
        
        return True 
    
    def bearishPin(self):
        if self.bearish(self.second):
            return False
        
        lowhighRange = abs(self.third['high'] - self.third['low'])
        topValue = max(self.third['open'], self.third['close'])
        if abs(topValue - self.third['low']) > lowhighRange * 0.33:
            return False
        
        return True 
    
    def oneWhiteSoldier(self):
        if self.bullish(self.second) or self.bearish(self.third):
            return False
        
        return (self.second['open'] < self.third['close']) and (self.second['close'] < self.third['open'])
    
    def oneBlackCrow(self):
        if self.bullish(self.third) or self.bearish(self.second):
            return False
        
        return (self.second['open'] > self.third['close']) and (self.second['close'] > self.third['open'])
    
    def morningStar(self):
        if self.bullish(self.first):
            return False;
        
        # gap down
        secondTopValue = max(self.second['close'], self.second['open'])
        if secondTopValue >= self.first['close']:
            return False
        
        # bullish 
        if self.bearish(self.third):
            return False
        
        # gap up
        if secondTopValue >= self.third['open']:
            return False
        
        # small body in the middle
        firstBody = self.first['open'] - self.first['close']
        secondBody = abs(self.second['open'] - self.second['close'])
        if secondBody > firstBody * 0.33:
            return False
        
        return True
    
    def eveningStar(self):
        if self.bearish(self.first):
            return False;
        
        if self.bullish(self.third):
            return False
        
        # gap up
        secondBottomValue = min(self.second['close'], self.second['open'])
        if secondBottomValue <= self.first['close']:
            return False
        
        # gap down
        if secondBottomValue <= self.third['open']:
            return False
        
        # small body in the middle
        firstBody = self.first['close'] - self.first['open']
        secondBody = abs(self.second['open'] - self.second['close'])
        if secondBody > firstBody * 0.33:
            return False
        
        return True
        
    def tweezerBottoms(self):
        if self.bullish(self.second):
            return False
        if self.bearish(self.third):
            return False
        
        bottomEqual = abs(self.second['close']-self.third['open']) <= max(abs(self.second['close']), abs(self.third['open'])) * 0.001
        topEqual = abs(self.second['open']-self.third['close']) <= max(abs(self.second['open']), abs(self.third['close'])) * 0.001
        
        return bottomEqual and topEqual
     
    def tweezerTops(self):
        if self.bullish(self.third):
            return False
        if self.bearish(self.second):
            return False   
        
        bottomEqual = abs(self.third['close']-self.second['open']) <= max(abs(self.third['close']), abs(self.second['open'])) * 0.001
        topEqual = abs(self.third['open']-self.second['close']) <= max(abs(self.third['open']), abs(self.second['close'])) * 0.001
        
        return bottomEqual and topEqual
     
    def bullishPattern(self):
        return self.tweezerBottoms() or self.bullishEngulf() or self.bullishPin() or self.oneWhiteSoldier() or self.morningStar()   
    
    def bearishPatter(self): 
        return self.tweezerTops() or self.bearishEngulf() or self.bearishPin() or self.oneBlackCrow() or self.eveningStar()
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     