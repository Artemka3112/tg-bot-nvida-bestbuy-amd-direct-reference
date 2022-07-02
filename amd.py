from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import threading, time
import settings
from items import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
threads = []
items = []



class Amd(threading.Thread):

	def __init__(self):
		super().__init__()
		self.iswork = True

	def run(self):
		# print(f"({time.ctime(time.time())}) - Start searching orders on Amd Direct")
		options = webdriver.ChromeOptions()
		options.page_load_strategy = 'eager'
		options.add_argument('--headless')
		options.add_argument('--no-sandbox')
		options.add_argument('--disable-dev-shm-usage')
		options.add_argument('--disable-gpu')
		#options.add_argument(f"--proxy-server={settings.proxys}:{settings.ports}")
		options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36")
		options.add_argument("--disable-blink-features=AutomationControlled")
		# profile = webdriver.FirefoxProfile()
		# profile.set_preference("network.proxy.type", 1)
		# profile.set_preference("network.proxy.http", settings.proxy)
		# profile.set_preference("network.proxy.http_port", settings.port)
		# profile.set_preference("network.proxy.ssl", settings.proxys)
		# profile.set_preference("network.proxy.ssl_port", settings.ports)
		# profile.set_preference('webdriver_enable_native_events', False)
		# profile.set_preference('browser.cache.memory.enable', False)
		# profile.set_preference('browser.sessionhistory.max_total_viewers', 0)
		# profile.set_preference('browser.sessionhistory.max_entries', 0)
		# profile.update_preferences()
		# while settings.amdenable and self.iswork:
		# 	try:
		self.driver = webdriver.Chrome(options=options)
		#time.sleep(10)
			# 	break
			# except Exception as e:
			# 	continue

		# while settings.amdenable and self.iswork:
		# 	try:
		self.driver.implicitly_wait(settings.amdtimeout)
		self.driver.get("https://www.amd.com/en/direct-buy/us")
		#time.sleep(10)
		time.sleep(3)
		try:
			trust = self.driver.find_element_by_class_name("onetrust-close-btn-ui")
			if not(trust == None):
				trust.click()
		except Exception as e:
			if settings.loggingexceptions:
				print("amd trust not found")
		self.driver.implicitly_wait(0)
			# 	break
			# except Exception as e:
			# 	continue
		while settings.amdenable and self.iswork:# can suicicde
			for item in items:
				self.driver.implicitly_wait(0)
				if not(self.iswork):
					break
				start = time.time()
				self.driver.get(item.order_url)
				#print(self.driver.page_source)
				if "Out of stock" in self.driver.page_source:
					time.sleep(settings.timeoutrefresh)
					end = time.time()
					if settings.loggerout:
						print(f'({time.ctime(time.time())}) - [amd] {item.order_name} - out ({round(end - start,3)}sec)')
					item.found = False
					continue
				elif "Add to cart" in self.driver.page_source:
					if not(settings.amdsimplemode):
						try:
							cart = self.driver.find_element_by_class_name("btn-shopping-cart")
							if not(cart == None):
								cart.click()
								self.driver.implicitly_wait(settings.amdtimeout)
								try:
										
									checkout = self.driver.find_element_by_class_name("checkout")# except when fake button
									if not(checkout == None):
										trash = self.driver.find_element_by_class_name("fa-trash").click()
										end = time.time()
										if settings.loggerout:
											print(f'({time.ctime(time.time())}) - [amd] {item.order_name} - ready for adding to cart ({round(end - start,3)}sec)')
										item.found = True
									else:
										end = time.time()
										print(f'({time.ctime(time.time())}) - [bb] {item.order_name} - out(by fake button) ({round(end - start,3)}sec)')
										item.found = False	
								except Exception as e:
									print(f'({time.ctime(time.time())}) - [bb] {item.order_name} - out(by fake button) ({round(end - start,3)}sec)')
									item.found = False	
						except Exception as e:
							if settings.loggingexceptions:
								print(self.driver.page_source)
								print(e)
							end = time.time()
							print(f'({time.ctime(time.time())}) - [bb] {item.order_name} - out(by exception) ({round(end - start,3)}sec)')
							item.found = False
						time.sleep(settings.timeoutrefresh)
						continue
					else:
						end = time.time()
						if settings.loggerout:
							print(f'({time.ctime(time.time())}) - [amd] {item.order_name} - ready for adding to cart ({round(end - start,3)}sec)')
						item.found = True
						time.sleep(settings.timeoutrefresh)
						continue
				else:
					end = time.time()
					if settings.loggerout:
						print(f'({time.ctime(time.time())}) - [amd] {item.order_name} - out ({round(end - start,3)}sec)')
					item.found = False
					time.sleep(settings.timeoutrefresh)
					continue
				driver.refresh()
			
		
		# print(f'({time.ctime(time.time())}) - Completing orders searching on Amd Direct')


	def stop(self):#deprecated
		self.iswork = False
		self.driver.close()


def startAmd() -> bool:
	if not(settings.amdenable):
		return True
	print(f"({time.ctime(time.time())}) - Starting Amd searching...")
	for name, order in settings.amd.items():
		i = AmdItem(name,order)
		print(f"({time.ctime(time.time())}) - Start search order {i.order_name} on Amd Direct")
		items.append(i)
	w = Amd()
	w.start()
	threads.append(w)
	return True
def stopAmd() -> bool:
	print(f"({time.ctime(time.time())}) - Stopping Amd searching...")
	while not(len(items) == 0):
		for item in items:
			print(f'({time.ctime(time.time())}) - Completing the order search {item.order_name} on Amd Direct')
			items.remove(item)
	while not(len(threads) == 0):
		for item in threads:
			item.stop()
			if item.is_alive():
				item.join()
			threads.remove(item)
	return True
def restartAmd() -> bool:
	stopAmd()
	startAmd()
	return True