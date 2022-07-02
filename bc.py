import threading, time
import amd, settings, bestbuy

threadbroadcaster = []
class Broadcaster(threading.Thread):
	def __init__(self):
		super().__init__()

	def run(self):
		print(f"({time.ctime(time.time())}) - Broadcaster started")

		while settings.broadcasting:
			for item in amd.threads:
				end = time.time()
				if (item.found) and (end - item.time > settings.msgtimeout):
					item.time = end
					if item.timebc - end <= 0:
						item.timebc = end + 60
						my_file = open("history.txt", 'a')
						my_file.write(f"\n({time.ctime(end)}) - [amd] {item.order_name} was in stock")
						my_file.close()
					print(f"\n({time.ctime(end)}) - [amd] {item.order_name} - IN STOCK BRO!!!!")
			for item in bestbuy.threads:
				end = time.time()
				if (item.found) and (end - item.time > settings.msgtimeout):
					item.time = end
					if item.timebc - end <= 0:
						item.timebc = end + 60
						my_file = open("history.txt", 'a')
						my_file.write(f"\n({time.ctime(end)}) - [bb] {item.order_name} was in stock")
						my_file.close()
					print(f"\n({time.ctime(end)}) - [bb] {item.order_name} - IN STOCK BRO!!!!")
		print(f"({time.ctime(time.time())}) - Broadcaster stopped")
	def stop(self):
		pass#("Broadcaster stopped")

def startBroadcaster():
	print(f"({time.ctime(time.time())}) - Starting broadcasting...")
	settings.broadcasting = True
	w = Broadcaster()
	w.start()
	threadbroadcaster.append(w)
def stopBroadcaster():
	print(f"({time.ctime(time.time())}) - Stopping broadcasting...")
	settings.broadcasting = False
	for item in threadbroadcaster:
		item.stop()
		item.join()
		threadbroadcaster.remove(item)