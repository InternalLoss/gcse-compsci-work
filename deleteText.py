# Project: Automated Readability Index
# Exam ID: 3500U30-1
# Unit 3 - Software Development Task.
# Candidate Name: Billy
# Description: Script to delete a text from the database.

import sqlite3,getpass,os,hashlib,datetime
import common # This is my own custom module with a few important functions.

conn = sqlite3.connect(common.dbFile) # This creates a connection to the file-based database.
c = conn.cursor() # The cursor is used to execute database commands.


print("*"*80) # 80 character lines are the default for IDLE.
#FIXTHIS: Change to be responsive to display.
print('''Text Deletion Script
Administrator use only.
Administrator account required.
''')
print("*"*80+"\n\n")
username = input("Enter your Username: ")
password = getpass.getpass("Enter your password: ")

# Begin Database Communication
t = (username,) # A tuple with the username variable bound as a string is a better idea than just inserting the string directly into the SQL query, which is unsafe.
c.execute('''SELECT * FROM users WHERE username=?''',t)
dbData = c.fetchone() # Only get one result for the username; if for some reason the username was duplicated, only the first record would be resolved.

# Begin authentication routines. #

if(dbData == None) : # If the username is not in the database.
	print("This username does not exist in our database.")
	exit()

if(dbData[2] < 1) : # If the user is not an administrator according to the database.
    print("You are not permitted to delete texts.")
    exit()
	
if(common.verifyPassword(dbData[1],password) == False): # Check the password against the database.
	print("Your password is not correct.")
	exit()



# End authentication routines; if a user gets to here, they're authenticated! #

print("Welcome %s"%(dbData[0]))
print("Beginning search.")
print("Options:")
print("1. Search by teacher's username.")
print("2. Search by keyword.")
option=input("Please enter your option => ")
if(option.isdigit()!=True): # If the option isn't a number.
	print("Your option was invalid.")
elif int(option) == 1:
	# Teacher name
	value=input("Please enter the name of the teacher => ")
	results = common.searchByTeacher(c,value)
	print("Search Results for Author %s"%(value))
	
	for array in results:
		print('*'*80)
		print("Unique ID: %s\nAuthor: %s\nEntry Date: %s\nTitle: %s\nText: %s"%(array[0],array[1],array[2],array[3],array[4]))
		print('*'*80+"\n")
elif int(option) == 2:
	# Keyword
	value=input("Please enter the keyword => ")
	results = common.searchByKeyword(c,value)
	print("Search Results for Keyword %s"%(value))
	for array in results:
		print('*'*80)
		print("Unique ID: %s\nAuthor: %s\nEntry Date: %s\nTitle: %s\nText: %s"%(array[0],array[1],array[2],array[3],array[4]))
		print('*'*80+"\n")

deleteID = input("Please enter the unique ID you wish to delete \n=> ")
t = (deleteID,)
c.execute("SELECT * FROM texts WHERE uuid = ?",t)
result = c.fetchone()
print("Unique ID: %s\nAuthor: %s\nEntry Date: %s\nTitle: %s\nText: %s"%(array[0],array[1],array[2],array[3],array[4]))
decision = input("Please confirm you wish to delete this text (y/N): ")

if(decision in ['y','Y']) :
	t = (datetime.date.today(),deleteID,username,)
	c.execute("INSERT INTO auditlog VALUES (?,?,?)",t)
	t = (deleteID,)
	c.execute("DELETE FROM texts WHERE uuid = ?",t)
	conn.commit() # Commit the actual changes to the file...
	conn.close()
	print("Deleted.")
elif(decision in ['n','N']):
	print("Cancelled.")
	exit()
else:
	print("Invalid answer; assuming no.")
	exit()
