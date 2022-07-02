import threading, time
import amd, bc, settings, bestbuy,restarter, userdata, server
import sys

class Commands(threading.Thread):
	def __init__(self):
		super().__init__()

	def run(self):
		#https://stackoverflow.com/questions/19479504/how-can-i-open-two-consoles-from-a-single-script
# 		p1 = Popen([sys.executable,"-c", """import sys
# for line in sys.stdin: # poor man's `cat`
# 	sys.stdout.write(line)
# 	sys.stdout.flush()
# """], stdin=PIPE, bufsize=1, universal_newlines=True,
#     # assume the parent script is started from a console itself e.g.,
#     # this code is _not_ run as a *.pyw file
#     creationflags=CREATE_NEW_CONSOLE)
# 		p1.stdin.write("Commands started")
# 		p1.stdin.flush()
		print(f"({time.ctime(time.time())}) - Commands started")
		while settings.inputcommands:
			command = input("Cmd: ")
			res = False
			if "stop" == command:
				res = amd.stopAmd()
				res = bestbuy.stopBestbuy()
			if "stop amd" == command:
				res = amd.stopAmd()
			if "stop bb" == command:
				res = bestbuy.stopBestbuy()
			if "stop server" == command:
				res = server.stopServer()

			if "start" == command:
				res = amd.startAmd()
				res = bestbuy.startBestbuy()
			if "start amd" == command:
				res = amd.startAmd()
			if "start bb" == command:
				res = bestbuy.startBestbuy()
			if "start server" == command:
				res = server.startServer()

			if "log" == command:
				if settings.loggingexceptions:
					settings.loggingexceptions = False
				else:
					settings.loggingexceptions = True
				res = True

			if "restart" == command:
				res = amd.restartAmd()
				res = bestbuy.restartBestbuy()
			if "restart amd" == command:
				res = amd.restartAmd()
			if "restart bb" == command:
				res = bestbuy.restartBestbuy()
			if "restart server" == command:
				res = server.restartServer()

			if "userdata" == command:
				for user in userdata.users:
					print(f"{user.id} - {user.ordertime}")
				res = True
			arr = command.split()
			if len(arr) == 4:
				if (arr[0] == "userdata") and (arr[1] == "add"):
					userdata.addUser(int(arr[2]),int(arr[3]))
					res = True
			if len(arr) == 3:
				if (arr[0] == "userdata") and (arr[1] == "del"):
					userdata.delUser(int(arr[2]))
					res = True

			if "close" == command:
				amd.stopAmd()
				bestbuy.stopBestbuy()
				server.stopServer()
				bc.stopBroadcaster()
				restarter.stopRestarter()
				userdata.writeUsers()
				res = True
				print("press ctrl + c")
				sys.exit(0)
				break
			if "bc" == command:
				if len(bc.threadbroadcaster) == 0:
					bc.startBroadcaster()
				else:
					bc.stopBroadcaster()
				res = True
			if "restarter" == command:
				if len(restarter.threadrestarter) == 0:
					restarter.startRestarter()
				else:
					restarter.stopRestarter()
				res = True
			if "help" == command:
				print(f"({time.ctime(time.time())}) - stop [amd,bb], start [amd,bb], restart [amd,bb], close, bc, check, userdata [del, add <id> <days>], restarter")
				res = True
			if "check" == command:
				msg = ""
				for item in amd.threads:
				    if (item.found):
				    	msg+=(f"({time.ctime(time.time())}) - [amd] \n{item.order_name} - ready for adding to cart")
				    else:
				    	msg+=(f"({time.ctime(time.time())}) - [amd] \n{item.order_name} - out")
				for item in bestbuy.threads:
				    if (item.found):
				    	msg+=(f"({time.ctime(time.time())}) - [bb] \n{item.order_name} - ready for adding to cart")
				    else:
				    	msg+=(f"({time.ctime(time.time())}) - [bb] \n{item.order_name} - out")
				res = True
				if msg == "":
					print(f"({time.ctime(time.time())}) - Empty")
				else:
					print(msg)
			if res:
				print(f"({time.ctime(time.time())}) - Done!")
			else:
				print(f"({time.ctime(time.time())}) - help to know commands or error")
			time.sleep(1)
		print(f"({time.ctime(time.time())}) - Commands stopped")

def startCommands():
	w = Commands()
	w.start()
