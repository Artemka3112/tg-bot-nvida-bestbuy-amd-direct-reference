from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import threading, time, sys
import settings

threads = []
class Bestbuy(threading.Thread):

	def __init__(self, order_name, order_url):
		super().__init__()
		self.order_name = order_name
		self.order_url = order_url
		self.waiting = False
		self.found = False
		self.time = 0
		self.timebc = 0
		self.iswork = True

	def run(self):
		print(f'({time.ctime(time.time())}) - Start search order {self.order_name} on Bestbuy')
		profile = webdriver.FirefoxProfile()
		profile.set_preference("intl.accept_languages", 'en-US, en')
		profile.set_preference("intl.locale.requested", 'en-US')
		profile.set_preference("browser.search.region", 'US')
		profile.set_preference("general.useragent.locale", 'en-US')
		profile.update_preferences()
		self.driver = webdriver.Firefox(firefox_profile=profile)
		self.driver.implicitly_wait(settings.bbtimeout)
		self.driver.get("https://www.bestbuy.com/")
		self.driver.find_element_by_class_name("us-link").click()
		self.driver.implicitly_wait(0)
		times = 0
		while settings.bbenable and self.iswork:
			start = time.time()
			self.driver.get(self.order_url)
			self.driver.execute_script("window.scrollTo(0, 70)") 
			try:
				if not(self.driver.find_element_by_class_name("add-to-cart-button").is_enabled()):
					time.sleep(settings.bbtimeoutrefresh)
					end = time.time()
					if settings.loggerout:
						print(f'({time.ctime(time.time())}) - [bb] {self.order_name} - out ({round(end - start,3)}sec)')
					self.found = False
					continue
				else:
					if settings.loggerout:
						print(f'({time.ctime(time.time())}) - [bb] {self.order_name} - ready for adding to cart')
					self.found = True
					continue
			except Exception as e:
				print(f'({time.ctime(time.time())}) - [bb] {self.order_name} - out(by exception)')
				times+=1
				if times == 5:
					w = Bestbuy(self.order_name,self.order_url)
					w.start()
					threads.append(w)
					break
				continue

		print(f'({time.ctime(time.time())}) - Completing the order search {self.order_name} on Bestbuy')
		self.stopt()

	def stop(self):
		if not(self.waiting == True):
			self.iswork = False
	def stopt(self):
		if not(self.waiting == True):
			self.driver.close()
			threads.remove(self)

def startBestbuy() -> bool:
	if not(settings.bbenable):
		return True
	print(f"({time.ctime(time.time())}) - Starting Bestbuy searching...")
	for name, order in settings.bestbuy.items():
		w = Bestbuy(name,order)
		w.start()
		threads.append(w)
	return True
def stopBestbuy() -> bool:
	print(f"({time.ctime(time.time())}) - Stopping Bestbuy searching...")
	while not(len(threads) == 0):
		for item in threads:
			item.stop()
			item.join()
	return True
def restartBestbuy() -> bool:
	stopBestbuy()
	startBestbuy()
	return True