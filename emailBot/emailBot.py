from imaplib import *
from emailBotInterface import *
import ssl
import re
from pprint import pprint
from  Models import *
from email.utils import parseaddr
import os

# from oauth2client import clientsecrets as clsr
# from . import googleOauth2 as go

class MailBot(BotInterface):
	"""docstring for MailBot"""
	folder = 'MailBot'
	port = 993

	__email_list = []
	spam_list = []

	__imap_server_dict = {}
	__imap_client_list = []

	login_flag = False
	done = False


	def __init__(self, email_object = None, spam_object = None):
		if(email_object != None):
			self.__email_list.append(email_object)
		if(spam_object != None):
			self.spam_list.append(spam_object)

	def __str__(self):
		return self.__doc__

	def set_email_list(self, List):
		self.__email_list = List

	def get_email_list(self):
		return self.__email_list

	def add_email(self,email_object):
		self.__email_list.append(email_object)

	def remove_email(self, email_object):
		self.__email_list.pop(self.__email_list.index(email_object))

	def add_spam(self,spam_object):
		self.spam_list.append(spam_object)

	def remove_spam(self,spam_object):
		self.spam_list.pop(self.spam_list.index(spam_object))


	def __parse(self, email_list = None):
		"""parse email to assign the right
			server
		"""
		index = 0
		email_list = self.__email_list
		
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

			self.__imap_server_dict[index] = server_addr
			index += 1

	def __spawn_imap_client(self):
		"""spawns an IMAP4_SSL object for
			each supplied user email
		"""
		self.__parse()
		self.__imap_client_list.clear()
		for key,host in self.__imap_server_dict.items():			
			try:				
				print("connecting....")
				print("to host at: %s"%host)				
				self.__imap_client_list.append(IMAP4_SSL(host,self.port))
				print("connected...")				
			except Exception as e:
				self.__imap_client_list.append(None)
				#print(e)
				print("Unable to connect to %s" %host)				


	def login(self, email_object = None, clients = None):
		"""Logs into server
		"""
		self.__spawn_imap_client();

		index = 0
		email_object = self.__email_list; clients = self.__imap_client_list

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


	def work(self, email_object = None, spam_object = None, clients = None, label = None):
		"""Deletes spam mails
		"""
		index = 0
		label = label if(label != None) else self.folder
		email_object = self.__email_list; spam_object = self.spam_list; clients = self.__imap_client_list
		
		if(len(email_object) == 1  and len(spam_object) == 1):	
			
			try:				
				if(clients[index] != None):
					clients[index].select(mailbox = label, readonly = False)
					junk,[IDs] = clients[index].search(None, '(FROM "flag")'.replace('flag',spam.get_id()))

					# print(type(IDs))
					IDs = IDs.decode('utf-8')

					if(IDs != '' and IDs != ' '):
						IDs = ','.join(IDs.split(' '))
						IDs = IDs.strip(',')					
					
						# print((IDs))
						clients[index].store(IDs,'+FLAGS','(\Deleted)')
						clients[index].expunge()
					self.done = True
			except IMAP4.error as e:				
				print("from work(): %s" % e)					

			except Exception as e:
				print("from work(): %s" % e)
		else:
			for spam in spam_object:
				for email in email_object:
					try:	
						if(clients[index] != None):
							junk, data = clients[index].select(mailbox = label, readonly = False)
							junk,[IDs] = clients[index].search(None, '(FROM "flag")'.replace('flag',spam.get_id()))
						
							# print(type(IDs))
							IDs = IDs.decode('utf-8')

							if(IDs != '' and IDs != ' '):
								IDs = ','.join(IDs.split(' '))
								IDs = IDs.strip(',')
						
								clients[index].store(IDs,'+FLAGS','(\Deleted)')
								clients[index].expunge()		
				
					except IMAP4.error as e:				
						print("from work(): %s" % e)					

					except Exception as e:
						print("from work(): %s" % e)
					finally:
						index += 1
				index = 0
			self.done = True

	def empty_spam(self):
		"""Empties folders in mail_box
		"""
		#Not working  for yahoo
		email_object = self.__email_list
		clients = self.__imap_client_list
		mail_box = ['Unsubscribe','Bulk Mail','Spam','Junk']
		index = 0
		for email in email_object:
			for box in mail_box:
				try:
					client = clients[index]
<<<<<<< HEAD
					if(client != None):
						client.select(mailbox = box, readonly = False)
						trash, IDs = client.search(None, 'NOT SEEN')	
						trash, ID = client.search(None, 'SEEN')
						IDs = IDs + ID

						IDs = IDs[0] + IDs[1]
						# print(type(IDs))		
						IDs = IDs.decode('utf-8')
						
						if(IDs != '' and IDs != ' '):
							IDs = ','.join(IDs.split(' '))
							IDs = IDs.strip(',')

							client.store(IDs,'+FLAGS','(\Deleted)')
							client.expunge()		
=======
					client.select(mailbox = box, readonly = False)
					trash, IDs = client.search(None, 'NOT SEEN')	
					trash, ID = client.search(None, 'SEEN')
					IDs = IDs + ID

					IDs = IDs[0] + IDs[1]
					# print(type(IDs))		
					IDs = IDs.decode('utf-8')
					if(IDs != '' and IDs != ' '):
						IDs = ','.join(IDs.split(' '))
						IDs = IDs.strip(',')

						client.store(IDs,'+FLAGS','(\Deleted)')
						client.expunge()		
>>>>>>> 3e3be6e138ed8d3f98754b15f27407a7d26cfcc7

				except IMAP4.error as e:				
					print("from empty_spam(): %s"%e)#"Operation failed!")					

				except Exception as e:
					print("from empty_spam(): %s" %e)		
			index += 1


	def add_folder(self, folder = None):
		"""inserts a folder 
		"""
		folder = folder if(folder != None) else "MailBot"
		flag = True
		clients  = self.__imap_client_list
		for client in clients:
			try:
				trash, data = client.list()
				for data in data:	
					if(folder in data.decode("utf-8") ):
						flag = False; break;
			
				if(flag):
					client.create(folder)
			except:
				pass
	
	# TODO: implement parse by sender name				
	def parse_mailbot(self, folder = None):
		"""parses emails in folder to retrieve
			email addresses
		"""
		clients = self.__imap_client_list
		folder = folder if(folder != None) else self.folder
		patterns = [
					"(\w+@\w+)\.(net|com|org|tv)",
					"(\w+\-\w+@\w+)\.(net|com|org|tv)",
					"(\w+@\w+\.\w+)\.(net|com|org|tv)",
					"(\w+@\w+\-\w+)\.(net|com|org|tv)",
					"(\w+\-\w+@\w+.\w+)\.(net|com|org|tv)",
					"(\w+\+\w+@\w+)\.(net|com|org|tv)"
					]
		obj = []
		for client in clients:			
			try:
				client.select(folder, False)				
				trash, IDs = client.search(None, 'NOT SEEN')	
				trash, ID = client.search(None, 'SEEN')
				IDs = IDs + ID

				IDs = IDs[0] + IDs[1]
				# print(IDs)

				# print(type(IDs))	
				IDs = IDs.decode('utf-8')
				IDs = ','.join(IDs.split(' '))
				IDs = IDs.strip(',')

				for ID in IDs.split(','):		
					trash, data = client.fetch(ID, '(BODY.PEEK[HEADER])')
					data = data[0]
					# pprint(data)
					for data in data:						
						data = data.decode("utf-8")
						# if(isinstance(data,tuple)):
						# print(parseaddr(data))
							# pprint(data[1])
						for pat in patterns:
							reg = re.compile(pat)
							if(len(reg.findall(data,2)) != 0):
								obj.append(reg.findall(data,2))
						

			except Exception as e:
				pass#rint("from parse_mailbot(): %s" % e)
		return obj		
				

 # SENTBEFORE <date>
 #         Messages whose [RFC-2822] Date: header (disregarding time and
 #         timezone) is earlier than the specified date.

	def parse_mailbot_helper(self, objs):
		"""processes the list of emails returned by 
			parse_mailbot()
		"""
		parsed = []		
		for obj in objs:
			for ob in obj:
				temp = '.'.join(ob)				
				parsed.append(temp)					
		parsed = list(set(parsed))
		# print(parsed)
		return parsed

	def add_parse_spam(self, parsed):
		"""adds the parsed email data from
			parse_mailbot_helper into 
			self.spam_list
		"""
		for email in self.__email_list:
			for spam in parsed:									
				if(email.get_email_addr() != spam):
					if(self.__in_list(self.spam_list,spam)):
						self.spam_list.append(Spam(spam))

	def __in_list(self,cont, email):
		"""prevents duplicate
			spam email
		"""
		for item in cont:
			if item.get_id() == email:
				return False
			else:
				return True


	def clean_up(self):	
		"""Logs out the bot"""
		for client in self.__imap_client_list:			
			if(client != None):
				try:
					client.close()
				except:
					pass
				client.logout()

