import socket, pickle, threading, time
import sys, signal
import items
import os
from prettytable import PrettyTable
from playsound import playsound

amd = []
bb = []

clients = []
alerts = []
		
datas = [b"data1", b"data2"]

soundalerts = True
soundalertscooldown = 1800

class Alert(threading.Thread):
	def __init__(self):
		super().__init__()
		self.iswork = True
	def run(self):
		while self.iswork:
			for item in amd:
				if item.found:
					playsound('found.mp3')
					time.sleep(soundalertscooldown)
					break
			for item in bb:
				if item.found:
					playsound('found.mp3')
					time.sleep(soundalertscooldown)
					break
	def stop(self):
		self.iswork = False

def startAlert():
	c = Alert()
	c.start()
	alerts.append(c)

def stopAlert():
	while not(len(alerts) == 0):
		for alert in alerts:
			alert.stop()
			alert.join()
		

class Client(threading.Thread):
	def __init__(self):
		super().__init__()
		self.iswork = True
		
		
	def run(self):
		self.sock = socket.socket()
		self.sock.connect(('127.0.0.1', 9090))
		global amd, bb
		BUFFER_SIZE = 4096
		self.sock.settimeout(2.0)
		while self.iswork:
			for cmd in datas:
				all_data = bytearray()
				self.sock.sendall(cmd)
				while True:
					try:
						data = self.sock.recv(BUFFER_SIZE)
						if not data:
							break
						#print('Recv: {}: {}'.format(len(data), data))
						all_data += data
					except socket.timeout:
						break
				#print('All data ({}): {}'.format(len(all_data), all_data))
				if not all_data:
					continue
				obj = pickle.loads(all_data)
				#print('Obj:', obj)
				
				if cmd == b"data1":
					amd = obj
				elif cmd == b"data2":
					bb = obj
		self.sock.close()
	def stop(self):
		self.iswork = False
		

def startClient():
	c = Client()
	c.start()
	clients.append(c)

def stopClient():
	while not(len(clients) == 0):
		for client in clients:
			client.stop()
			client.join()

def signal_handling(signum,frame):
	stopClient()
	stopAlert()
	sys.exit(0)

startClient()
startAlert()
signal.signal(signal.SIGINT,signal_handling)

def getString(found) -> str:
	if found:
		return colored(102,255,0,"IN STOCK")
	else:
		return colored(245,0,41,"OUT")

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

while True:
	os.system('cls')
	mytable = PrettyTable()
	mytable.field_names = ["Site", "Item", "Stock"]
	for item in amd:
		mytable.add_row(["Amd Direct", item.order_name, getString(item.found)])
	for item in bb:
		mytable.add_row(["BestBuy", item.order_name, getString(item.found)])
	print(mytable)
	print(f"Sound alerts - {soundalerts}")
	time.sleep(2)
