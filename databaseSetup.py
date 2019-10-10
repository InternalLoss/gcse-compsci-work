# Project: Automated Readability Index
# Exam ID: 3500U30-1
# Unit 3 - Software Development Task.
# Candidate Name: Billy
# Description: This program creates a database with the valid tables for use in the program.
# * if a blank database is used, createAdmin.py will need to be ran to create an admin account to subsequently make a teacher account.
import sqlite3, common


conn = sqlite3.connect(common.dbFile) # This creates a connection to the file-based database.
c = conn.cursor() # The cursor is used to execute database commands.

c.execute('''CREATE TABLE texts (uuid text REQUIRED, author text REQUIRED, entry_date date REQUIRED, keywords text, text text REQUIRED, calculatedReadingIndex float REQUIRED, intendedReadingIndex int REQUIRED)''') # Create the table for the texts.
c.execute('''CREATE TABLE users (username text REQUIRED, password text REQUIRED, type int REQUIRED default 0) ''') # Create the user table for authentication.
c.execute('''CREATE TABLE auditlog (deletion_date date REQUIRED, text_uuid text REQUIRED, deletion_user text REQUIRED)''') # Create the audit log table.
 
conn.commit() # Commit the actual changes to the file...
conn.close() # ...and subsequently close the file.

print("Database created!")