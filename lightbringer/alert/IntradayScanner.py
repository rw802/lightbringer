from IntraDay import IntraDay
import Config as cfg
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

inputPath = '../scan/ScanIn5Min.txt'
ti = TechIndicators(key=cfg.APIKey, output_format=cfg.format)
ts = TimeSeries(key=cfg.APIKey, output_format=cfg.format)
inqueryInterval = cfg.interval5
schedulerInterval = 30

intraDayFiveMin = IntraDay(
    symbolFilePath = inputPath, 
    avTimeSeriesObj=ts, 
    avTechIndicatorObj=ti, 
    inqueryInterval=inqueryInterval, 
    schedulerInterval=schedulerInterval,
    channel = "exit_alert"
    )

intraDayFiveMin.runBullishCheck(CandleMustBull = True)
