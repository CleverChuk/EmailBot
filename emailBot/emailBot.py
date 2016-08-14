from imaplib import *
from emailBotInterface import *
import ssl
import re
# from oauth2client import clientsecrets as clsr
# from . import googleOauth2 as go


pattern = "\w+@\w+\.(com|net|org)"
regObj = re.compile(pattern)


class MailBot(BotInterface):
	"""docstring for MailBot"""
	folder = 'INBOX'
	port = 993

	email_list = []
	spam_list = []

	imap_server_dict = {}
	imap_client_list = []

	login_flag = False


	def __init__(self, email_object, spam_object):
		self.email_list.append(email_object)
		self.spam_list.append(spam_object)

	def __str__(self):
		return self.__doc__

	def add_email(self,email_object):
		self.email_list.append(email_object)

	def remove_email(self, email_object):
		self.email_list.pop(self.email_list.index(email_object))

	def add_spam(self,spam_object):
		self.spam_list.append(spam_object)

	def remove_spam(self,spam_object):
		self.spam_list.pop(self.spam_list.index(spam_object))


	def __parse(self, email_list = None):
		index = 0
		email_list = self.email_list

		for email in email_list:	
			email = email.get_email_addr()			
			loc = email.find('@') + 1

			if('yahoo' in email):
				server_addr = 'imap.mail.'+ email[loc:]
			elif('outlook' in email or 'hotmail' in email):
				if('hotmail' in email):
					email = email.replace('hotmail','outlook')
				server_addr = 'imap-mail.'+ email[loc:]
			elif('gmail' in email):
				server_addr = 'imap.'+ email[loc:]
			else:
				server_addr = None

			self.imap_server_dict[index] = server_addr
			print(self.imap_server_dict)
			index += 1

	def __spawn_imap_client(self):
		self.__parse()

		for key,host in self.imap_server_dict.items():			
			try:				
				print("connecting....")
				print("to host at: %s"%host)				
				self.imap_client_list.append(IMAP4_SSL(host,self.port))
				print("connected...")				
			except Exception as e:
				self.imap_client_list.append(None)
				print(e)
				print("Unable to connect to %s" %host)				


	def login(self, email_object = None, clients = None):
		self.__spawn_imap_client();

		index = 0
		email_object = self.email_list; clients = self.imap_client_list

		if(len(email_object) == 1):				
			if(clients[index] != None):
				clients[index].login(email_object[index].get_email_addr(), email_object[index].get_pass())				
				self.login_flag = True
		else:
			for email in email_object:
				if(clients[index] != None):
					clients[index].login(email.get_email_addr(), email.get_pass())
					self.login_flag = True
				index += 1


	def work(self, email_object = None, spam_object = None, clients = None):
		index = 0
		email_object = self.email_list; spam_object = self.spam_list; clients = self.imap_client_list
		
		if(len(email_object) == 1  and len(spam_object) == 1):	
			try:
				# print(spam_object[index].get_id())					
				clients[index].select(mailbox = self.folder, readonly = False)
				junk,[IDs] = clients[index].search(None, '(FROM "flag")'.replace('flag',spam_object[index].get_id()))
				IDs = IDs.decode('utf-8')
				IDs = ','.join(IDs.split(' '))
				clients[index].store(IDs,'+FLAGS','(\Deleted)')
				clients[index].expunge()
			
			except IMAP4.error:				
				print("Operation failed!")					

			except Exception as e:
				print(e)
		else:
			for spam in spam_object:
				for email in email_object:
					try:						
						junk, data = clients[index].select(mailbox = self.folder, readonly = False)
						junk,[IDs] = clients[index].search(None, '(FROM "flag")'.replace('flag',spam.get_id()))
						IDs = IDs.decode('utf-8')
						IDs = ','.join(IDs.split(' '))
						clients[index].store(IDs,'+FLAGS','(\Deleted)')
						clients[index].expunge()		
				
					except IMAP4.error:				
						print("Operation failed!")					

					except Exception as e:
						print(e)
					finally:
						index += 1
				index = 0

	def clean_up(self):	
		for client in imap_client_list:
			if(client != None):
				client.logout()

