from emailBot import *
from Models  import *



if __name__ == '__main__':		
	gmail = Email("your email");
	gmail.set_pass()

	email_list = []
	

	gmail_spam = Spam("your spammer1")
	gmail_spam2 = Spam("your spammer1")

	spam_list = []

	Bot = MailBot(gmail, gmail_spam)
	Bot.add_spam(gmail_spam2)

	Bot.login()

	while(True):
		if(Bot.login_flag):
			Bot.work()
		else:
			print("No work to do!")
			break
