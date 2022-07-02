from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import threading, time, sys
import settings
from items import *
from selenium.webdriver.chrome.options import Options

threads = []
items = []


class Bestbuy(threading.Thread):

	def __init__(self):
		super().__init__()
		self.iswork = True

	def run(self):
		print(f'({time.ctime(time.time())}) - Start searching orders on Bestbuy')
		options = webdriver.ChromeOptions()
		options.page_load_strategy = 'eager'
		options.add_argument('--headless')
		options.add_argument('--no-sandbox')
		options.add_argument('--disable-dev-shm-usage')
		options.add_argument('intl.accept_languages')
		options.add_argument('--lang=en-US')
		options.add_argument('--disable-gpu')
		options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36")
		options.add_argument("--disable-blink-features=AutomationControlled")
		#options.add_argument(f"--proxy-server={settings.proxys}:{settings.ports}")
		self.driver = webdriver.Chrome(options=options)
		# options = Options()
		# options.add_argument('-headless')
		# profile = webdriver.FirefoxProfile()
		# profile.set_preference("intl.accept_languages", 'en-US, en')
		# profile.set_preference("intl.locale.requested", 'en-US')
		# profile.set_preference("browser.search.region", 'US')
		# profile.set_preference("general.useragent.locale", 'en-US')
		# profile.set_preference('webdriver_enable_native_events', False)
		# profile.set_preference('browser.cache.memory.enable', False)
		# profile.set_preference('browser.sessionhistory.max_total_viewers', 0)
		# profile.set_preference('browser.sessionhistory.max_entries', 0)
		# profile.update_preferences()
		# while settings.bbenable and self.iswork:
		# 	try:
		
		#time.sleep(10)
		# 		break
		# 	except Exception as e:
		# 		continue
		# while settings.bbenable and self.iswork:
		# 	try:
		self.driver.implicitly_wait(settings.bbtimeout)
		self.driver.get("https://www.bestbuy.com/")
		#time.sleep(10)
		try:
			self.driver.find_element_by_class_name("us-link").click()
		except Exception as e:
			pass
		self.driver.implicitly_wait(0)
			# 	break
			# except Exception as e:
			# 	continue
		# times = 0
		while settings.bbenable and self.iswork:
			for item in items:
				self.driver.implicitly_wait(0)
				if not(self.iswork):
					break
				start = time.time()
				self.driver.get(item.order_url)
				self.driver.execute_script("window.scrollTo(0, 70)") 

				try:
					if not(self.driver.find_element_by_class_name("btn-disabled") == None):
						time.sleep(settings.bbtimeoutrefresh)
						end = time.time()
						if settings.loggerout:
							print(f'({time.ctime(time.time())}) - [bb] {item.order_name} - out ({round(end - start,3)}sec)')
						item.found = False
						continue
				except Exception as e:
					pass
				try:
					time.sleep(1)
					cart = self.driver.find_element_by_class_name("add-to-cart-button")
					if not(cart.is_enabled()):
						time.sleep(settings.bbtimeoutrefresh)
						end = time.time()
						if settings.loggerout:
							print(f'({time.ctime(time.time())}) - [bb] {item.order_name} - out ({round(end - start,3)}sec)')
						item.found = False
						continue
					elif cart.is_enabled():
						cart.click()
						time.sleep(1)
						if "Please Wait" in self.driver.page_source:
							end = time.time()
							if settings.loggerout:
								print(f'({time.ctime(time.time())}) - [bb] {item.order_name} - ready for adding to cart ({round(end - start,3)}sec)')
							item.found = True
							time.sleep(settings.bbtimeoutrefresh)
							continue
						elif "Sold Out" in self.driver.page_source:
							time.sleep(settings.bbtimeoutrefresh)
							end = time.time()
							if settings.loggerout:
								print(f'({time.ctime(time.time())}) - [bb] {item.order_name} - out ({round(end - start,3)}sec)')
							item.found = False
							continue



						self.driver.implicitly_wait(8)
						gcart = self.driver.find_element_by_class_name("go-to-cart-button")
						if not(gcart == None):
							gcart.click()
							self.driver.find_element_by_class_name("cart-item__remove").click()
							end = time.time()
							if settings.loggerout:
								print(f'({time.ctime(time.time())}) - [bb] {item.order_name} - ready for adding to cart ({round(end - start,3)}sec)')
							item.found = True
							time.sleep(settings.bbtimeoutrefresh)
							continue
						else:
							time.sleep(settings.bbtimeoutrefresh)
							end = time.time()
							if settings.loggerout:
								print(f'({time.ctime(time.time())}) - [bb] {item.order_name} - out ({round(end - start,3)}sec)')
							item.found = False
							continue
				except Exception as e:
					end = time.time()
					if settings.loggingexceptions:
						print(e)
					print(f'({time.ctime(time.time())}) - [bb] {item.order_name} - out(by exception) ({round(end - start,3)}sec)')
					# times+=1
					# if times == 5:
					# 	w = Bestbuy(self.order_name,self.order_url)
					# 	w.start()
					# 	threads.append(w)
					# 	break
					continue

		print(f'({time.ctime(time.time())}) - Completing orders searching on Bestbuy')

	def stop(self):
		self.iswork = False
		self.driver.close()
def startBestbuy() -> bool:
	if not(settings.bbenable):
		return True
	print(f"({time.ctime(time.time())}) - Starting Bestbuy searching...")
	for name, order in settings.bestbuy.items():
		i = BestbuyItem(name,order)
		print(f'({time.ctime(time.time())}) - Start search order {i.order_name} on Bestbuy')
		items.append(i)
	w = Bestbuy()
	w.start()
	threads.append(w)
	return True
def stopBestbuy() -> bool:
	print(f"({time.ctime(time.time())}) - Stopping Bestbuy searching...")
	while not(len(items) == 0):
		for item in items:
			print(f'({time.ctime(time.time())}) - Completing the order search {item.order_name} on Bestbuy')
			items.remove(item)
	while not(len(threads) == 0):
		for item in threads:
			item.stop()
			if item.is_alive():
				item.join()
			threads.remove(item)
	return True
def restartBestbuy() -> bool:
	stopBestbuy()
	startBestbuy()
	return True