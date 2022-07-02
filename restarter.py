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
			global timestart
			if timestart == 0:
				timestart = time.time()
				continue
			end = time.time()
			if end - timestart == settings.restartcooldown:
				print(f"({time.ctime(time.time())}) - Time for restarting")
				timestart = end.time()
				amd.restartAmd()
				bestbuy.restartBestbuy()
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