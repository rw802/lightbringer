class Strategy(object):
    def __init__(self, avTechIndicatorObj):
        self.avTechIndicatorObj = avTechIndicatorObj
        
    def verify(self):
        raise NotImplementedError # see subclasses for implementation