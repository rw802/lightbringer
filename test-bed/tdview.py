import requests, json
from decimal import Decimal
import colorama
from colorama import Fore, Back, Style



class Scanner(object):

	def __init__(self):
		colorama.init()
		self.headers = {
			'Origin': 'https://www.tradingview.com',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'en-US,en;q=0.8',
			'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Accept': 'application/json, text/javascript, */*; q=0.01',
			'Referer': 'https://www.tradingview.com/markets/cryptocurrencies/quotes-all/',
			'Connection': 'keep-alive',
		}

		self.dataBTRX = '{"filter":[{"left":"Recommend.All","operation":"nempty"},{"left":"exchange","operation":"equal","right":"BITTREX"}],"symbols":{"query":{"types":[]}},"columns":["name","close","change","change_abs","volume","Recommend.All","exchange","description","name","subtype"],"sort":{"sortBy":"Recommend.All","sortOrder":"desc"},"options":{"lang":"en"},"range":[0,1000]}'

	def scraper(self):
		s = requests.Session()
		page = s.post('https://scanner.tradingview.com/crypto/scan', headers=self.headers, data=self.dataBTRX)
		#print(json.dumps(page.json(), indent=5))
		page = page.text
		jason = json.loads(page)
		return jason

	def escape(self,num):
		num = Decimal(num)
		num = str(num)
		num = num[0:11]
		return num

	def centered(self,text):
		return '{:^30}'.format(text)

	def centered1(self,text):
		return '{:^40}'.format(text)

	def double_centered(self,text):
		return '{:^60}'.format(text)

	def kleen_data(self,pair,close,change,change_abs,volume):
		try:

			print (self.centered('Pair :')+self.centered(pair))

			color_close = self.green_red(close)
			print (self.centered('Close :')+self.centered1(color_close))


			color_change = self.green_red(change)
			print (self.centered('Change :')+self.centered1(color_change))


			color_abs = self.green_red(change_abs)
			print (self.centered('Change_ABS :')+self.centered1(color_abs))

			print (self.centered('Volume : ')+ self.centered(volume))

			print ('\n\n')
		except Exception as BudLight:
			print (BudLight)
			pass

	def green_red(self,number):
		if Decimal(number) < 0:
			return(Fore.RED + str(number) + Style.RESET_ALL)
		if Decimal(number) > 0:
			return(Fore.GREEN + str(number) + Style.RESET_ALL)

	def parse_data(self,data):
		for item in data[u'data']:
			combo_site_pair = item[u's']
			pair_info = item[u'd']

			close = pair_info[1]
			close = self.escape(close)

			change = pair_info[2]
			#change = self.escape(close)

			change_abs = pair_info[3]
			change_abs = self.escape(change_abs)


			volume = pair_info[4]

			self.kleen_data(combo_site_pair,close,change,change_abs,volume)
			#print ('{0}\nClose : {1}\nChange : {2}\nChange Abs : {3}\nVolume : {4}\n'.format(combo_site_pair,close,change,str(change_abs),volume))

	def run(self):
		print(self.double_centered('KJ TradingView QuotesBot'))
		data = self.scraper()
		self.parse_data(data)

instance = Scanner()
runner = instance.run()
