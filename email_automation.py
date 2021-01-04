import time
import schedule
from datetime import datetime
import random
import json
import smtplib
import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import ast

#my imports 
from email_counter import email_count
import config
import csv

# Login / email credentials
user = config.EMAIL_ADDRESS
password = config.EMAIL_PASSWORD
imap_url = 'imap.gmail.com'
email_counter = 3

# Gmail auth setup
con = imaplib.IMAP4_SSL(imap_url)
con.login(user,password)

con.select('INBOX')

result, data = con.fetch(b'1','(RFC822)')
raw = email.message_from_bytes(data[0][1])

# Create the correct ordinal suffix for the number of each message
def ordinal_suffix(self):
		suffix = ""
		if self == 1:
			suffix = "st"
		elif self == 2:
			suffix = "nd"
		elif self == 3:
			suffix = "rd"
		elif self > 20 and i % 10 == 1:
			suffix = "st"
		elif self > 20 and i % 10 == 2:
			suffix = "nd"
		elif self > 20 and i % 10 == 3:
			suffix = "rd"
		else:
			suffix = "th"
		return suffix

# Creates a subject line
def subject_line(self):
	if self <= 100:
		return (f"Your {self}{ordinal_suffix(self)} letter")
	elif self > 100:
		remainder = self % 100 
		return (f"Your {self}{ordinal_suffix(remainder)} letter")

# Calls a random quote from a json file of quotes I scraped
def create_message():
    with open('JSON FILEPATH ') as f:
    	quotes_dict = json.load(f)
    	random_quote = quotes_dict[f"{random.randint(1, len(quotes_dict))}"]
    	random_quote_formatted = random_quote.encode('ascii', 'ignore').decode('ascii')

    well_wishes = [
    				"Hey Mom, hope youre doing awesome :)\n",
    				"Hey Hey!\n",
    				"Just checking in...\n",
    				"How's it going?\n",
    				"Good morning, today's going to rock!\n",
    				"Just emailing again about your letter writing resolution\n",
    				"Hope you're staying consistent!\n"
    ]
    accountability = [
    				"Who did you write to today?\n",
    				"Who are you going to write today?\n",
    				"Who did you compliment today in your letter?\n",
    				"Two questions today: 1.Who are you going to write? 2.How is your motivation/morale doing?\n"
    ]

    # Creates a random message and uses conditional logic to ask about previous emails sent.
    file = open("recieved_emails_dictionary.py", "r")
    contents = file.read()
    emails_dictionary = ast.literal_eval(contents)
    file.close()
    try:
        email_name = emails_dictionary[email_counter-14]['name']
    except KeyError:
        email_name = None
    callback = ""
    if email_name != None:
        callback = f"Hey, how did {email_name} take your letter a while back?\n"
        msg_body = random.choice(well_wishes)+random.choice(accountability)+callback+random_quote_formatted
        return msg_body
    else:
        msg_body = random.choice(well_wishes)+random.choice(accountability)+random_quote_formatted
        return msg_body      

#Setsup a secure connection with gmail and sends an email
def send_email():
	global email_counter
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls() 
	s.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
	subject = subject_line(email_counter)
	message = 'Subject:{}\n\n{}'.format(subject, create_message())
	s.sendmail(config.EMAIL_ADDRESS, "SEND TO THIS ADDRESS", message)
	s.quit() 
	email_counter += 1 

# Sets up another connection and gets my email
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None,True)

# Search for a particular email
def search(key,value,con):
    result, data  = con.search(None,key,'"{}"'.format(value))
    return data
    #extracts emails from byte array

# Gets messages into list   
def get_emails(result_bytes):
    msgs = []
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, '(RFC822)')
        msgs.append(data)
    return msgs

# Checks an email for any common names and returns the name 
def check_name(email):
    name_list = [line.rstrip('\n') for line in open("2000_most_popular_first_names.py")]
    for name in name_list:
        if name in email:
            return name
            
def emails_to_dictionary():
    #gets all messages from my email from my mom 
    msgs = get_emails(search('FROM',"FROM RECIPIENT",con))
    messages_dict = {}
    messages_dict_pos = 1
    # Makes a list of my email inbox
    for msg in msgs:
        email_body = get_body(email.message_from_bytes(msg[0][1]))
        email_name= check_name(email_body.decode("utf-8"))
        messages_dict[messages_dict_pos] = {"name":email_name,"body":email_body}
        messages_dict_pos += 1
    with open("recieved_emails_dictionary.py", 'w') as f: 
        f.write('{\n')
        for key, value in messages_dict.items(): 
            f.write('%s:%s,\n' % (key, value))
        f.write('}')

#15 Write readme, Submit to GitHub with a mille high overview of what this software does and also what I learned by making it 

# Keeps an active loop running until a year has elapsed and sends an email, daily
schedule.every().hour.do(emails_to_dictionary)
# schedule.every().day.at("04:32").do(send_email)
schedule.every(3).minutes.do(send_email)
while email_counter < 366:
    schedule.run_pending()
    time.sleep(1)