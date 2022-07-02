

class AmdItem:
	def __init__(self, order_name, order_url):
		super().__init__()
		self.order_name = order_name
		self.order_url = order_url
		self.waiting = False
		self.found = False
		self.time = 0
		self.timebc = 0
		
class BestbuyItem:
	def __init__(self, order_name, order_url):
		super().__init__()
		self.order_name = order_name
		self.order_url = order_url
		self.waiting = False
		self.found = False
		self.time = 0
		self.timebc = 0