# Sort of header file for the emailBot design

class BotInterface:
	"""Interface that defines the contract for the bot design"""	
	def spawn_imap_client(self):
		"""spawns new imap client to do jobs"""
		raise NotImplementedError

	def login(self):
		"""logins into the server and work"""
		raise NotImplementedError
	
	def work(self):
		pass

	def clean_up(self):
		"""Logs the bot out of the server"""
		raise NotImplementedError


class Except(Exception):
	"""Defines exceptions raised by Bots that implements the above 
		interface"""
	msg = {
			"email":"Invalid email address",
			"login":"Unable to login",
			"server":"server not responding"
			}
	key = None
	value = None

	def __init__(self, key):
		self.key = key
		self.value = self.msg[key]

	def __str__(self):
		return self.value

