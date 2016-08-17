from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

# Set up your Consumer and Token as per usual. Just like any other
# three-legged OAuth request.
consumer = oauth.Consumer('your_consumer_key', 'your_consumer_secret')
token = oauth.Token('your_users_3_legged_token', 
    'your_users_3_legged_token_secret')

# Setup the URL according to Google's XOAUTH implementation. Be sure
# to replace the email here with the appropriate email address that
# you wish to access.
url = "https://mail.google.com/mail/b/your_users_email@gmail.com/imap/"

conn = imaplib.IMAP4_SSL('imap.googlemail.com')
conn.debug = 4 

# This is the only thing in the API for impaplib.IMAP4_SSL that has 
# changed. You now authenticate with the URL, consumer, and token.
conn.authenticate(url, consumer, token)

# Once authenticated everything from the impalib.IMAP4_SSL class will 
# work as per usual without any modification to your code.
conn.select('INBOX')
print(conn.list())