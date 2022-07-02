import socket, pickle, time, threading
import settings, amd, bestbuy

threadservers = []
class Server(threading.Thread):
	def __init__(self):
		super().__init__()
		self.iswork = True

	def run(self):
		print(f"({time.ctime(time.time())}) - Server started")
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(settings.ip)
		self.sock.listen(settings.listeners)


		while self.iswork:
			conn, addr = self.sock.accept()
			print( f"({time.ctime(time.time())}) - gui connected")
			conn.settimeout(settings.connecttimeout)
			while True:
				try:
					data = conn.recv(4096)
					if not data:
						break
					if data == b"data1":
						data1 = pickle.dumps(amd.items)
						conn.sendall(data1)
					elif data == b"data2":
						data2 = pickle.dumps(bestbuy.items)
						conn.sendall(data2)
				except Exception as e:
					break
			print( f"({time.ctime(time.time())}) - gui disconnected")
			conn.close()

		if not(self.iswork):
			self.sock.shutdown(socket.SHUT_RDWR)
			self.sock.close()
		print(f"({time.ctime(time.time())}) - Server stopped")
	def stop(self):
		self.iswork = False
		self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()

def startServer() -> bool:
	if not(settings.server):
		return True
	print(f"({time.ctime(time.time())}) - Starting server...")
	w = Server()
	w.start()
	threadservers.append(w)
	return True

def stopServer() -> bool:
	print(f"({time.ctime(time.time())}) - Stopping server...")
	for item in threadservers:
		item.stop()
		item.join()
		threadservers.remove(item)
	return True
def restartServer() -> bool:
	stopServer()
	startServer()
	return True
