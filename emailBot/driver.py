#!/user/bin/env python3
from emailBot import *
from Models  import *
import Models
import time
import os
import atexit
# This script uses the emailBot and Models Model to 
# implement a simple imapclient that filters unwanted emals 
# added to the folder Created by the script

# Yahoo Mail: No problem as of yet
# Gmail: Needs to turn on less secure app. Working on using Oauth
# Other mails: Not tested yet
def save_state(obj,filename):
	with open(filename,'wb') as file:
		Models.save_instance(obj,file)
		file.close()

if __name__ == '__main__':	

	if(os.path.exists("./EmailBot")):
		os.chdir("./EmailBot")
	else:
		os.mkdir("EmailBot")
		os.chdir("EmailBot")

	spam_file = "./Spammers.pickle"
	email_file = "./email.pickle"

	email_list = [] # add email addresses
	
	# add spam emails or email address or you can just run this script it 
	# will add a MailBot folder then move all email you want to filter out into
	# the folder.
	spam_list = []		
	
	Bot = MailBot()
	try:
		if(os.path.exists(email_file)):
			with open(spam_file,'rb') as s_file:
				with open(email_file,'rb') as e_file:
					Bot.spam_list = Models.load_instance(s_file)
					e_List = Models.load_instance(e_file)

					Bot.set_email_list(e_List)
					s_file.close()
					e_file.close()
					# Models.print_list(Bot.spam_list)
					# print((Bot.get_email_list())[0].get_email_addr())
					while(True):
						Bot.login()
						if(Bot.login_flag):
							Bot.add_folder()
							obj = Bot.parse_mailbot() #err
							obj = Bot.parse_mailbot_helper(obj)
							
							Bot.add_parse_spam(obj)			
							Bot.work()
							Bot.work(label='INBOX')

							if(Bot.done):
								Bot.empty_spam()
								Bot.clean_up()
								save_state(Bot.get_email_list(),email_file)
								save_state(Bot.spam_list,spam_file)
								time.sleep(10)
						else:
							print("No work to do!")
							break
			# save_state(Bot)
		else:

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
					Bot.work(label='INBOX')

					if(Bot.done):
						# Bot.empty_spam()
						Bot.clean_up()
						save_state(Bot.get_email_list(),email_file)
						save_state(Bot.spam_list,spam_file)
						time.sleep(10)
				else:
					print("No work to do!")
					break
	except KeyboardInterrupt:
		 atexit.register(save_state,obj = Bot.spam_list, filename = spam_file)
		 atexit.register(save_state,obj = Bot.get_email_list(), filename = email_file)
		 exit(0)

