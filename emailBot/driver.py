from emailBot import *
from Models  import *
import time
# This script uses the emailBot and Models Model to 
# implement a simple imapclient that filters unwanted emals 
# added to the folder Created by the script

# Yahoo Mail: No problem as of yet
# Gmail: Needs to turn on less secure app. Working on using Oauth
# Other mails: Not tested yet

if __name__ == '__main__':		

	email_list = [] # add email addresses
	# add spam emails or email address or you can just run this script it 
	# will add a MailBot folder then move all email you want to filter out into
	# the folder.
	spam_list = []	

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
				Bot.empty_spam()
				Bot.clean_up()
				time.sleep(round(10**3) + 3)
		else:
			print("No work to do!")
			break
