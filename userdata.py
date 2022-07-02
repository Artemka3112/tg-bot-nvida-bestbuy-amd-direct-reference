import pickle, time



class User:
	def __init__(self,id,ordertime):
		self.id = id
		self.ordertime = time.time() + ordertime*24*60*60
		self.timer = 0
		self.timerbb = 0

users = []



def loadUsers():
	global users
	users = []
	for clas in pickle.load(open("users", "rb")):
		users.append(clas)
		#print(f"{clas.id} - {clas.ordertime}")

def writeUsers():
	pickle.dump(users, open("users", "wb"))

def updateUsers():
	writeUsers()
	loadUsers()

def addUser(id, days):
	for user in users:
		if (user.id == id) and (user.ordertime - time.time() > 0):
			user.ordertime+=days*24*60*60
			print(f"({time.ctime(time.time())}) - {id} add {days} days")
			updateUsers()
			return
		elif (user.id == id) and (user.ordertime - time.time() <= 0):
			user.ordertime = time.time() + days*24*60*60
			print(f"({time.ctime(time.time())}) - {id} refreshed {days} days")
			updateUsers()
			return
	u = User(id,days)
	users.append(u)
	print(f"({time.ctime(time.time())}) - {id} created with {days} days")
	updateUsers()

def delUser(id):
	for user in users:
		if (user.id == id):
			users.remove(user)
			print(f"({time.ctime(time.time())}) - user {id} deleted")
			updateUsers()
			return
	print(f"({time.ctime(time.time())}) - unexisted user")
	

#users.append(123)
#writeUsers()
# loadUsers()
# addUser(1243,123)
# for user in users:
# 	print(f"{user.id} - {user.ordertime}")