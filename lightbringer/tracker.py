#! /usr/bin/python3

import random
import time
import datetime
import curses
from curses.textpad import Textbox, rectangle
import traceback
import json
import pandas
import os
import sys
import urllib
import logging
from functools import wraps
import humanfriendly

# imports for Alpha Vantage stuff
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.sectorperformance import SectorPerformances


# imports for apscheduler
from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

COLOR_DEFAULT = 0
COLOR_GREEN = 84
COLOR_RED = 197
COLOR_GREY = 241

# global vars
g_period_map = {
    '1min': 60,
        '5min': 300,
        '15min': 900,
        '30min': 1800,
        '60min': 3600
}
g_periods = []
g_symbols = []
g_columns = ['time', 'close', 'diffvol', 'ema', 'rsi', 'range']
g_mainwin = None
g_panels = {}

# panel obj


class Cell(object):

    def __init__(self, win=None):
        self.win = win
        self.val = 'N/A'
        self.row = -1
        self.col = -1
        self.h = 1
        self.w = 1
        self.color = COLOR_DEFAULT


# std obj
class StdOutWrapper(object):

    def __init__(self):
        self.text = ""

    def write(self, txt):
        self.text += txt
        self.text = '\n'.join(self.text.split('\n')[-30:])

    def get_text(self, beg=None, end=None):
        return '\n'.join(self.text.split('\n')[beg:end])

    def save(self):
        with open('log.txt', 'w') as f:
            f.write(self.text)


# apsche stuff
executors = {'default': {'type': 'threadpool', 'max_workers': 30},
             'processpool': ProcessPoolExecutor(max_workers=5)
             }
job_defaults = {'coalesce': True,
                'max_instances': 3
                }
g_scheduler = BackgroundScheduler()
g_scheduler.configure(
    executors=executors, job_defaults=job_defaults, timezone=utc)

# Alpha Advantage handlers
g_data = {}  # global data cache
g_ti = None
g_sp = None
g_ts = None
MAX_API_RETRIES = 3


# ti params
ema_fast_period = 4
ema_slow_period = 8

# print the last operation to console line


def print_to_console(func, msg=None):
    logmsg = msg if msg else func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        if g_mainwin:
            win.move(3, 1)
            win.clrtoeol()
            win.addstr(logmsg)
            win.refresh()
        return ret
    return wrapper


@print_to_console
def setup_av(path='../docs/config/my_info_2.json'):
    global g_ts, g_ti, g_sp

    # Read API infos from config
    try:
        with open(path, 'r') as f:
            info = json.load(f)
            ALPHAVANTAGE_API_TOKEN = info['alphavantage']['key']

            g_ts = TimeSeries(
                key=ALPHAVANTAGE_API_TOKEN, output_format='pandas')
            g_ti = TechIndicators(
                key=ALPHAVANTAGE_API_TOKEN, output_format='pandas')
            g_sp = SectorPerformances(
                key=ALPHAVANTAGE_API_TOKEN, output_format='pandas')

    except Exception as e:
        print ('Unable to setup Alpha Vantage')
        exit(-1)


# @print_to_console
def update_symbol(symbol, period):
    """ Update a symbol

    Updating symbol consists of fetching data from AV and
    refreshing the corresponding UI tables

    """

    while True:
        if fetch_symbol(symbol, period):
            break
        time.sleep(1)
    update_ui_symbol(symbol, period)


@print_to_console
def fetch_symbol(symbol, period):
    """ Fetch data matrix of a symbol from AV

    """
    global g_data, g_ts, g_ti, g_sp
    # return close and color

    def cal_close(ts):
        d = ts[0].tail(2)['close']
        ret0 = str(d[-1])
        ret1 = COLOR_DEFAULT

        if d[-1] > d[-2]:
            ret1 = COLOR_GREEN
        elif d[-1] < d[-2]:
            ret1 = COLOR_RED
        return ret0, ret1

    # return time
    def cal_time(ts):
        return ts[1]['3. Last Refreshed'][-8:-3], COLOR_DEFAULT

    # return volume difference from 20 avg and color
    def cal_vol(ts):
        d = ts[0].tail(21)['volume']
        v = d[-1]
        avgv = d[-21:-1].mean()
        val = v - avgv
        ret0 = humanfriendly.format_size(v)
        a = ret0.split()
        if len(a) == 2:
            ret0 = a[0]
            ss = a[1][0]
            if a[1].startswith('K'):
                ret0 += ' k'
            elif a[1].startswith('M'):
                ret0 += ' m'
            elif ss == 'G':
                ret0 += ' g'
        ret1 = COLOR_DEFAULT

        if v > 1.3 * avgv:
            ret1 = COLOR_GREEN
        elif v < 0.7 * avgv:
            ret1 = COLOR_RED
        return ret0, ret1

    def cal_rsi(feed):
        d = feed[0].tail(2)['RSI']
        ret0 = str(d[-1])
        ret1 = COLOR_DEFAULT

        if d[-1] > d[-2]:
            ret1 = COLOR_GREEN
        elif d[-1] < d[-2]:
            ret1 = COLOR_RED
        return ret0, ret1

    def two_seg_compare(f4, f8):
        """
        Compare the trend of two segments, can be used for ema,
        price, ...
        @param f4: bullish seg
        @param f8: bearish seg
        """

        # crossing
        if f4[-1] > f8[-1] and f4[-2] < f8[-2]:
            return 'X', COLOR_GREEN
        if f4[-1] < f8[-1] and f4[-2] > f8[-2]:
            return 'X', COLOR_RED

        d = 0
        grades = {-2: 215, -3: 206, -4: 197, 2: 76, 3: 52, 4: 47}
        # uptreding
        if f4[-1] > f8[-1]:
            d += 2
            if f4[-1] > f4[-2]:
                d += 1
            if f8[-1] > f8[-2]:
                d += 1
            return str(f4[-1]), grades[d]
        # downtrending
        if f4[-1] < f8[-1]:
            d -= 2
            if f4[-1] < f4[-2]:
                d -= 1
            if f8[-1] < f8[-2]:
                d -= 1
            return str(f8[-1]), grades[d]

        return 'N/A', COLOR_DEFAULT

    def cal_ema(feed4, feed8):
        f4 = feed4[0].tail(2)['EMA']
        f8 = feed8[0].tail(2)['EMA']

        return two_seg_compare(f4, f8)

    # def cal_macd(feed):
    #     macd = feed[0].tail(1)['MACD']
    #     macd_sig = feed[0].tail(1)['MACD_Signal']

    #     return two_seg_compare(macd, macd_sig)

    def cal_range(ts, window=8):
        """
        return the low and high in given window
        """
        vlow = ts[0].tail(window)['low']
        vhigh = ts[0].tail(window)['high']
        ret0 = ''
        ret1 = COLOR_DEFAULT

        low = min(x for x in vlow)
        high = max(x for x in vhigh)
        ret0 += str(low) + '/' + str(high)

        return ret0, ret1

# 'time'  :None,
# 'close' :None,
# 'diffvol'   :None,
# 'ema'   :None,
# 'macd'  :None,
# 'rsi'   :None,
# 'cci'   :None,
# 'macd'  :None
    try:
        handle = g_data[symbol][period]

        if period == 'daily':
            ts = g_ts.get_daily(symbol=symbol)
        else:
            ts = g_ts.get_intraday(symbol=symbol, interval=period)

        c = handle['close']
        if c:
            c.val, c.color = cal_close(ts)
        c = handle['diffvol']
        if c:
            c.val, c.color = cal_vol(ts)
        c = handle['time']
        if c:
            c.val, c.color = cal_time(ts)
        c = handle['range']
        if c:
            c.val, c.color = cal_range(ts)

        c = handle['rsi']
        if c:
            feed = g_ti.get_rsi(symbol=symbol, interval=period)
            c.val, c.color = cal_rsi(feed)
        c = handle['ema']
        if c:
            feed4 = g_ti.get_ema(symbol=symbol, interval=period, time_period=4)
            feed8 = g_ti.get_ema(symbol=symbol, interval=period, time_period=8)
            c.val, c.color = cal_ema(feed4, feed8)
        # c = handle['macd']
        # if c:
        #     feed = g_ti.get_macd(symbol=symbol, interval=period)
        #     c.val, c.color = cal_macd(feed)

        return True

    # except KeyError as e:
    #     logging.warning("[{}] is not supported by Alpha Vantage.".format(symbol))
    #     return False

    # except urllib.error.HTTPError:  # Alpha Vantage API has high failure rate - retry 3 times
    #     logging.error("[{}] - Exception HTTPError - Retry: {}/{}".format(
    #         symbol, retry_count, MAX_API_RETRIES))
    #     return False

    except Exception as e:
        logging.warning("[{}] is not updated.".format(symbol))
        return False


@print_to_console
def update_ui_symbol(symbol, period=None):
    """ Update newly fetched data to UI

    """
    global g_data, g_ts, g_ti, g_sp

    # update real-time quotes from RH at the first row
    if not period:
        pass

    # update technical indicators from AV
    else:
        handle = g_data[symbol][period]
        for each in g_columns:
            c = handle[each]
            w = c.win
            w.addstr(c.row, c.col, '          ')
            w.addstr(c.row, c.col, c.val, curses.color_pair(c.color))
            w.refresh()


def setup_panels(win):
    """ Condigure panel for each symbol

    This function adds an item that keys a symbol (str),values  a panel (obj),
    and field (str) - coordinates (int tuple) to g_panels

    """

    global g_symbols, g_panels, g_periods

    # number of symbols + 2 for boarders + 1 for period
    subwin_height = len(g_periods) + 3
    # 5 for console display
    x0, y0 = 5, 0
    sx, sy = subwin_height, 120

    for symbol in g_symbols:
        subwin = win.subwin(sx, sy, x0, y0)
        g_panels[symbol] = subwin
        g_data[symbol]['panel'] = subwin
        subwin.nodelay(1)  # disable getch() blocking
        subwin.erase()
        subwin.bkgdset(' ')
        subwin.border()

        row = 1
        col = 1
        subwin.addstr(row, col, symbol)
        col += 10
        for each in g_columns:
            subwin.addstr(row, col, each)
            col += 10

        row = 2
        for period in g_periods:
            col = 1
            subwin.addstr(row, col, period)
            col += 10
            for each in g_columns:
                cell = g_data[symbol][period][each]
                cell.win = subwin
                cell.row = row
                cell.col = col
                cell.h = 1
                cell.w = 10
                if each == 'range':
                    cell.w = 16
                col += cell.w

            update_ui_symbol(symbol, period)
            row += 1

        subwin.refresh()
        x0 += subwin_height


# generate the main display
def setup_mainwin(win):
    win.erase()

    win.move(1, 1)
    win.addstr("Team kotrt Monitor")
    win.move(2, 1)
    win.addstr('Console Output: ')
    win.refresh()


def mainloop(win):
    """ main loop of the app

    """

    global g_periods, g_symbols, g_data, g_scheduler, g_period_map

    win.nodelay(1)  # disable getch() blocking
    # draw the main display template
    setup_mainwin(win)
    # setup alpha vantage readers
    setup_av()
    # load periods and symbols from config file
    load_config()
    # setup panels for symbols loaded from config
    setup_panels(win)

    # manually update before starting jobs
    for period in g_periods:
        for symbol in g_symbols:
            update_symbol(symbol, period)

    # add job for each symbol that has a panel
    c = 1
    jobs = []
    for period in g_periods:
        for symbol in g_symbols:
            id = symbol + '_' + period
            job = g_scheduler.add_job(
                func=update_symbol,
                    trigger='interval',
                    args=[symbol, period],
                    seconds=int(g_period_map[period] / 3),
                    id=id
            )
            c += 1
    # start worker
    g_scheduler.start()

    # check active jobs
    # jobs = g_scheduler.print_jobs()

    # run until the user wants to quit
    while 1:
        # check for keyboard input
        inch = win.getch()
        # getch() will return -1 if no character is available
        if inch != -1:
            # see if inch is really a character
            try:
                instr = str(chr(inch))
            except:
                # just ignore non-character input
                pass
            else:
                if instr.upper() == 'U':
                    refresh_ui()
                if instr.upper() == 'Q':
                    g_scheduler.shutdown(wait=False)
                    break
        # keyboard response rate
        time.sleep(0.05)


@print_to_console
def load_config(p='../docs/config/tracker_layout.json'):
    global g_symbols, g_periods, g_data

    with open(p, 'r') as f:
        d = json.load(f)
        g_symbols = d["symbols"]
        g_periods = d["windows"]

    for symbol in g_symbols:
        g_data[symbol] = {}
        for period in g_periods:
            g_data[symbol][period] = {x: Cell() for x in g_columns}


def setup_color_pairs():
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)


def startup():
    # borrowed the idea of using a try-except wrapper around the
    # initialization from David Mertz.
    try:
        # Initialize curses
        stdscr = curses.initscr()

        curses.start_color()
        curses.use_default_colors()
        # color setup
        curses.has_color = curses.has_colors()
        if curses.has_color:
            if curses.COLORS < 8:
                # not colourful enough
                curses.has_color = False
            setup_color_pairs()

        # Turn off echoing of keys, and enter cbreak mode,
        # where no buffering is performed on keyboard input
        curses.noecho()
        curses.cbreak()

        mainloop(stdscr)                # Enter the main loop

        # Set everything back to normal
        curses.echo()
        curses.nocbreak()

        curses.endwin()                 # Terminate curses
    except:
        # In event of error, restore terminal to sane state.
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        traceback.print_exc()           # Print the exception

if __name__ == '__main__':

    # setup_av()
    # print (g_ts.get_intraday(symbol='AMD', interval='1min'))
    mystdout = StdOutWrapper()
    sys.stdout = mystdout
    sys.stderr = mystdout

    startup()

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    sys.stdout.write(mystdout.get_text())
    mystdout.save()
