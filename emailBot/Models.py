import getpass
import pickle
class Email(object):
	"""Emmail class """
	_email_addr = None
	_pass = None

	def __init__(self,addr):
		self._email_addr = addr

	def set_email_addr(self, addr):
		self._email_addr = addr;

	def get_email_addr(self):
		return self._email_addr

	def set_pass(self):
		self._pass = getpass.getpass()

	def get_pass(self):
		return self._pass

	def __str__(self):
		return ("Email class")

class Spam(object):
	"""Spam class"""
	_id = None
	
	def __init__(self, id):
		self._id = id

	def set_id(self, id):
		self._id = id

	def get_id(self):
		return self._id


	def __str__(self):
		return ("Spam class")


def save_instance(obj, file):
	pickle.dump(obj,file)

def load_instance(file):
	return pickle.load(file)
