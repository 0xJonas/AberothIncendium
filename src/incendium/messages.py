class Command:
	
	def get_id():
		pass;
		
	def get_length():
		pass
	
class Message:

	def __init__(self,time=-1):
		self.time=time;
		
	def get_id():
		pass;
		
	def get_length():
		pass

class CreateWindow(Message):
	
	def get_id():
		return 0x14;
	
	def get_length():
		pass;