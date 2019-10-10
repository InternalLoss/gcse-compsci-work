# Project: Automated Readability Index
# Exam ID: 3500U30-1
# Unit 3 - Software Development Task.
# Candidate Name: Billy
# Description: The main script! This one handles insertion, and search, as well as login for teachers (admins can also login, but they cannot do anything admin-specific.)

import sqlite3,common,getpass,math,uuid,datetime # SQLite for database, common is my own module, getpass for password entry without echoing, math for math.ceil, uuid for the unique IDs, and datetime to allow for dates to be stored in DB.

def addTextRoutine():
	print("Beginning Text Entry.")
	title=input("Please enter the title of the text\n=> ")
	valid=False
	while valid == False:
		intAge=input("Please enter the intended age of the text.\n=> ")
		try:
			intAge = int(intAge)
			valid = True
		except:
			print("You have entered an invalid age.")
	keyword=input("Please enter a keyword to search by\n=>" )
	valid = False
	while valid == False:
		text=input("Please enter the text=>\n") #FIXTHIS: Does not handle new lines.
		char=common.countCharacters(text)
		word=common.countWords(text)
		sent=common.countSentences(text)
		if(sent < 1 or word < 1): # There needs to be at least a word, a sentence, and a character for the text to be valid.
			print("Your text is invalid.")
		else:
			valid = True
	calcARI = (4.71*(char/word)+0.5*(word/sent)-21.43) # Calculate the overall ARI in float form
	roundARI = math.ceil(calcARI) # This /always/ rounds up. 5.1 will become 6, etc
	print('\n\n'+'*'*80+'\n\n')
	print("Title: %s"%title)
	print("Intended Reading Age: %i"%intAge)
	print("ARI's Calculated Age: %s"%(common.calcAge(roundARI)))
	print("Keyword: %s"%keyword)
	print("Text:\n%s"%text)
	confirm=input("Do you want to confirm submission? (y/N): ")
	if confirm in ["Y","y"]:
		# Add the text!
		textUUID = str(uuid.uuid4())
		t = (textUUID,username,datetime.date.today(),keyword,text,intAge,roundARI)
		c.execute('''INSERT INTO texts VALUES (?,?,?,?,?,?,?) ''',t)
		conn.commit() # Commit the actual changes to the file...
		print("Your text has been added.")
	else:
		print("Submission cancelled.")

def searchTextRoutine():
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

	
print('*'*80) # 80 character lines are the default for IDLE.
print('''Text Store
Copyright (C) Generic School Solutions, 2019
Version x.y.z alpha
Licensed to Fanta Sea School.
''')
print('*'*80+'\n\n')

username = input('Enter your Username: ')
password = getpass.getpass('Enter your password: ')
conn = sqlite3.connect(common.dbFile) # This creates a connection to the file-based database.
c = conn.cursor()

# Begin Database Communication
t = (username,) # A tuple with the username variable bound as a string is a better idea than just inserting the string directly into the SQL query, which is unsafe.
c.execute('''SELECT * FROM users WHERE username=?''',t)
dbData = c.fetchone() # Only get one result for the username; if for some reason the username was duplicated, only the first record would be resolved.

# Begin authentication routines. #

if(dbData == None) : # If the username is not in the database.
	print('This username does not exist in our database.')
	exit()

if(common.verifyPassword(dbData[1],password) == False): # Check the password against the database; if it's false...
	print('Your password is not correct.')
	exit()

# End authentication routines; if a user gets to here, they're authenticated! #

print('Welcome, %s.'%(dbData[0]))
while True:
	print('Your current options are:')
	print('1. Enter a new text')
	print('2. Search for a text')
	print('3. Exit')
	option = input('Please enter an option (1-3): ')

	if(option.isdigit()!=True): # If the option isn't a number.
		print("Your option was invalid.")
	elif int(option) == 1:
		# Create Text
		addTextRoutine()
	elif int(option) == 2:
		# Search for a text.
		searchTextRoutine()
	elif int(option) == 3:
		conn.close() # ...and subsequently close the file.
		exit()
	else: # If the option isn't 1-3 but IS a number.
		print('Invalid option selected.')
