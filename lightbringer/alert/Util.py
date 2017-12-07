SMA = 'SMA'
EMA = 'EMA'

MABull =        1 << 0
BBandBull =     1 << 1
RSIBull =       1 << 2
CandleBull =    1 << 3
MACDBull =      1 << 4

def printInK(num):
    return int((num/1000)).__str__() + 'K'

def readIntoList(path):
    symbols = []
    for line in open(path):
        columns = line.split(' ')
        if len(columns) >= 1:
            symbols.append(columns[0])
    return symbols

def isBullish(input, target):
    return (input & target) != 0

def setBullish(input, target):
    input |= target
    