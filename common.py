# Project: Automated Readability Index
# Exam ID: 3500U30-1
# Unit 3 - Software Development Task.
# Candidate Name: Billy
# Description: Common file with variables used in most scripts, as well as common functions.

import hashlib

scores = [
[1,"5-6","Year 1"],
[2,"6-7","Year 2"],
[3,"7-8","Year 3"],
[4,"8-9","Year 4"],
[5,"9-10","Year 5"],
[6,"10-11","Year 6"],
[7,"11-12","Year 7"],
[8,"12-13","Year 8"],
[9,"13-14","Year 9"],
[10,"14-15","Year 10"],
[11,"15-16","Year 11"],
[12,"16-17","Year 12"],
[13,"17-18","Year 13"],
]

# Path of database file (absolute or relative file path - ie, "file.db", "../file.db", "/usr/local/file.db", "C:\file.db", etcetera)
dbFile = "database.db"

# Connection to DB could be placed in here, however due to it requiring 2 lines no matter what I do, it would be of little use.

## Authentication Functions
def createPassword(plaintext): # SHA256 encoded password.
	return hashlib.sha256(plaintext.encode('utf-8')).hexdigest()

def verifyPassword(hash,plaintext): # Returns True or False.
	return hash == hashlib.sha256(plaintext.encode('utf-8')).hexdigest()

def createUser(c,username,password): # This code assumes that the variable c (a cursor for database manipulation) is already bound in the script, and has to be referenced when executed.
	insertpass=createPassword(password) # This hashes the new password for insertion into the database.
	t=(username,insertpass) # This tuple ensures it's correctly bound.
	c.execute('''INSERT INTO users VALUES (?,?,0) ''',t)

## ARI Functions
def countCharacters(content):
	return len(content)

def countWords (content):
	return len(content.split())

def countSentences(content):
	return content.count(".")+content.count("?")+content.count("!") # Punctuation marks usually mark the end of a sentence.

def calcAge(ari):
	if(ari > 13):
		return "18+" # The score list doesn't go any further than 17-18 (13), so if above this then give a generic "18+" result just in case the text is too long.
	else:
		return scores[ari-1][1] # This references the array of the datastore (arrays start at 0)'s second column (the age)

## Database Lookup Functions
def searchByTeacher(c,value):
	t=(value,)
	c.execute("SELECT * FROM texts WHERE author = ?",t)
	result=c.fetchall() # Get /all/ results for the query.
	return result

def searchByKeyword(c,value):
	t=(value,)
	c.execute("SELECT * FROM texts WHERE keywords = ?",t)
	result=c.fetchall() # Get /all/ results for the query.
	return result