from IntraDay import IntraDay
import Config as cfg
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

inputPath = '../scan/hold.txt'
ti = TechIndicators(key=cfg.APIKey, output_format=cfg.format)
ts = TimeSeries(key=cfg.APIKey, output_format=cfg.format)
inqueryInterval = cfg.interval30
schedulerInterval = 5*60

exitChecker = IntraDay(
    symbolFilePath = inputPath, 
    avTimeSeriesObj=ts, 
    avTechIndicatorObj=ti, 
    inqueryInterval=inqueryInterval, 
    schedulerInterval=schedulerInterval,
    channel = "exit_alert"
    )

exitChecker.runBearishCheck(CandleMustBear = True)
