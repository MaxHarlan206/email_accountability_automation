# email_accountability_automation

WHY DID I MAKE IT?
My mothers 2021 new years resolution was to write a kind letter every day to someone close to her.
This email automation program was built to keep her motivated. 
It is running 24/7 on a Google Compute Engine. 

WHAT DOES IT DO? 
This program keeps her accountable with a message randomly generated from a list of salutations, a list of questions to keep her motivated, a list of quotes about writing which I created through a simple web scraper, and (if relevant) a sentence asking how the person she wrote 2 weeks prior reacted to her letter. 
It scans her incoming messages and stores the email bodies, and the name of anyone who she mentioned in the email in a python dictionary of dictioniaries. 

WHAT IS IT BUILT WITH?
Google Compute Engine
Python json, time, schedule, random, imaplib, and stmplib
