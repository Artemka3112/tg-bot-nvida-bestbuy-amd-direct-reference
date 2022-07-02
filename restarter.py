import settings, amd, bestbuy
import threading, time

timestart = 0
threadrestarter = []
class Restarter(threading.Thread):
	def __init__(self):
		super().__init__()

	def run(self):
		print(f"({time.ctime(time.time())}) - Restarter started")
		while settings.restarting:
			try:
				global timestart
				if timestart == 0:
					timestart = time.time()
					continue
				end = time.time()
				if end - timestart >= settings.restartcooldown:
					print(f"({time.ctime(time.time())}) - Time for restarting")
					timestart = end
					amd.restartAmd()
					bestbuy.restartBestbuy()
				for item in amd.threads:
					if not(item.is_alive()):
						amd.restartAmd()
				for item in bestbuy.threads:
					if not(item.is_alive()):
						bestbuy.restartBestbuy()
			except Exception as e:
				pass
			time.sleep(1)
		print(f"({time.ctime(time.time())}) - Restarter stopped")
	def stop(self):
		pass#("Restarter stopped")

def startRestarter():
	print(f"({time.ctime(time.time())}) - Starting restarter...")
	settings.restarting = True
	w = Restarter()
	w.start()
	threadrestarter.append(w)
def stopRestarter():
	print(f"({time.ctime(time.time())}) - Stopping restarter...")
	settings.restarting = False
	for item in threadrestarter:
		item.stop()
		item.join()
		threadrestarter.remove(item)