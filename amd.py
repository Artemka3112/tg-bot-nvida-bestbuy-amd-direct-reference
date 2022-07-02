from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import threading, time
import settings


threads = []
class Amd(threading.Thread):

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
		print(f"({time.ctime(time.time())}) - Start search order {self.order_name} on Amd Direct")
		profile = webdriver.FirefoxProfile()
		profile.set_preference("network.proxy.type", 1)
		profile.set_preference("network.proxy.http", settings.proxy)
		profile.set_preference("network.proxy.http_port", settings.port)
		profile.set_preference("network.proxy.ssl", settings.proxys)
		profile.set_preference("network.proxy.ssl_port", settings.ports)
		profile.update_preferences()
		self.driver = webdriver.Firefox(firefox_profile=profile)


		self.driver.get(self.order_url)
		self.driver.implicitly_wait(5)
		time.sleep(3)
		self.driver.find_element_by_class_name("onetrust-close-btn-ui").click()
		self.driver.implicitly_wait(0)
		while settings.amdenable and self.iswork:# can suicicde
			start = time.time()
			self.driver.get(self.order_url)
			if "Out of stock" in self.driver.page_source:
				time.sleep(settings.timeoutrefresh)
				end = time.time()
				if settings.loggerout:
					print(f'({time.ctime(time.time())}) - [amd] {self.order_name} - out ({round(end - start,3)}sec)')
				self.found = False
				continue
			else:
				if settings.loggerout:
					print(f'({time.ctime(time.time())}) - [amd] {self.order_name} - ready for adding to cart')
				self.found = True
				break
			
		
		print(f'({time.ctime(time.time())}) - Completing the order search {self.order_name} on Amd Direct')
		self.stopt()
	def stop(self):#deprecated
		if not(self.waiting == True):
			self.iswork = False
	def stopt(self):
		if not(self.waiting == True):
			self.driver.close()
			threads.remove(self)


def startAmd() -> bool:
	if not(settings.amdenable):
		return True
	print(f"({time.ctime(time.time())}) - Starting Amd searching...")
	for name, order in settings.amd.items():
		w = Amd(name,order)
		w.start()
		threads.append(w)
	return True
def stopAmd() -> bool:
	print(f"({time.ctime(time.time())}) - Stopping Amd searching...")
	while not(len(threads) == 0):
		for item in threads:
			item.stop()
			item.join()
	return True
def restartAmd() -> bool:
	stopAmd()
	startAmd()
	return True