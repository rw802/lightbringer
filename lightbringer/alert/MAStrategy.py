from Strategy import Strategy
import Util as util

class MAStrategy(Strategy):
    def __init__(self, avTechIndicatorObj):
        Strategy.__init__(self, avTechIndicatorObj)
        self.function = {util.SMA:avTechIndicatorObj.get_sma, util.EMA:avTechIndicatorObj.get_ema}
        
    def verify(self, symbol, interval = 'daily', timePeriodShort = 50, timePeriodLong = 150, value = 'close', type = util.SMA):
        try:
            dataShort, meta_data = self.function[type](symbol = symbol, interval = interval, time_period = timePeriodShort, series_type = value)
            dataLong, meta_data = self.function[type](symbol = symbol, interval = interval, time_period = timePeriodLong, series_type = value)
        except:
            return False

        if dataLong[type][-1] >= dataShort[type][-1]:
            return False
#         elif dataLong[type][-10] > dataLong[type][-1] or dataShort[type][-10] > dataShort[type][-1]:
#             return False
        else:
            return True
        
