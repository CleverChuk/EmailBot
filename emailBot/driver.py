#!user/bin/env python
from emailBot import *
from Models  import *
import Models
import time
import os
# This script uses the emailBot and Models Model to 
# implement a simple imapclient that filters unwanted emals 
# added to the folder Created by the script

# Yahoo Mail: No problem as of yet
# Gmail: Needs to turn on less secure app. Working on using Oauth
# Other mails: Not tested yet
def save_state(obj):
	with open(filename,'wb') as file:
		Models.save_instance(obj,file)
		file.close()

if __name__ == '__main__':	

	if(os.path.exists("./EmailBot")):
		os.chdir("./EmailBot")
	else:
		os.mkdir("EmailBot")
		os.chdir("EmailBot")

	filename = "./Spammers.bat"

	email_list = [] # add email addresses
	
	# add spam emails or email address or you can just run this script it 
	# will add a MailBot folder then move all email you want to filter out into
	# the folder.
	spam_list = []	

	if(os.path.exists(filename)):
		with open(filename,'rb') as file:
			Bot = Models.load_instance(file)
			file.close()
			# print(Bot.e_list)
			while(True):
				Bot.login()
				if(Bot.login_flag):
					Bot.add_folder()
					obj = Bot.parse_mailbot() #err
					obj = Bot.parse_mailbot_helper(obj)
					
					Bot.add_parse_spam(obj)			
					Bot.work()

					if(Bot.done):
						# Bot.empty_spam()
						Bot.clean_up()
						save_state(Bot)
						time.sleep(round(10**3) + 3)
				else:
					print("No work to do!")
					break
		# save_state(Bot)
	else:

		Bot = MailBot()
		for email in email_list:
			email = Email(email)
			print("Enter password for %s" % email.get_email_addr())
			email.set_pass()

			Bot.add_email(email)

		for spam in spam_list:
			
			spam = Spam(spam)		
			Bot.add_spam(spam)
		
		
		while(True):
			Bot.login()
			if(Bot.login_flag):

				Bot.add_folder()
				obj = Bot.parse_mailbot() #err
				obj = Bot.parse_mailbot_helper(obj)
				
				Bot.add_parse_spam(obj)			
				Bot.work()

				if(Bot.done):
					# Bot.empty_spam()
					Bot.clean_up()
					save_state(Bot)
					time.sleep(round(10**3) + 3)
			else:
				print("No work to do!")
				break

# atexit.register(save_state,Bot)

