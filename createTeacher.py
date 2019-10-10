# Project: Automated Readability Index
# Exam ID: 3500U30-1
# Unit 3 - Software Development Task.
# Candidate Name: Billy
# Description: Script to add a new user to the database; an admin account is required to do so, which can be made using createAdmin.py

import sqlite3,getpass,os,hashlib
import common # This is my own custom module with a few important functions.

conn = sqlite3.connect(common.dbFile) # This creates a connection to the file-based database.
c = conn.cursor() # The cursor is used to execute database commands.


print("*"*80) # 80 character lines are the default for IDLE.
#FIXTHIS: Change to be responsive to display.
print('''User Creation Script
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

if(common.verifyPassword(dbData[1],password) == False): # Check the password against the database.
	print("Your password is not correct.")
	exit()


if(dbData[2] < 1) : # If the user is not an administrator according to the database.
    print("You are not permitted to add new user accounts.")
    exit()

# End authentication routines; if a user gets to here, they're authenticated! #

print("Welcome %s"%(dbData[0]))
# First, add the new user.
newuser = input("Please enter the username for the new teacher: ")
newpassword = input("Please enter their password: ")
common.createUser(c,newuser,newpassword)
conn.commit()


print("Thank you. User %s has now been added."%(newuser))

# Now, ask if they want to add more (batch user adding is such a good idea for administrators)
while True:
	decision=input("Do you want to add another user? (y/n)")
	if(decision in ['y','Y']) :
		newuser = input("Please enter the username for the new teacher: ")
		newpassword = input("Please enter their password: ")
		common.createUser(c,newuser,newpassword)
		conn.commit()
		print("Thank you. User %s has now been added."%(newuser))
		# User returns to line 58 until N is pressed.
	elif(decision in ['n','N']):
		print("Logging out and exiting.")
		exit()
	else:
		print("Invalid answer; assuming no for security reasons.")
		exit()