# Project: Automated Readability Index
# Exam ID: 3500U30-1
# Unit 3 - Software Development Task.
# Candidate Name: Billy
# Description: Create an Administrator Account, which is allowed to login to the main script interface, as well as create user accounts.

import sqlite3,common,getpass
conn = sqlite3.connect(common.dbFile) # This creates a connection to the file-based database.
c = conn.cursor() # The cursor is used to execute database commands.
username = input("Admin Username: ")
plainpass = getpass.getpass("Admin Password: ")

hashpass = common.createPassword(plainpass)
t = (username,hashpass)
c.execute('''INSERT INTO users VALUES (?,?,1) ''',t) # Binding to a tuple is safer - any number above 0 has admin privileges (Useful for if, say, IT admins vs Head of English has a different role and further implementation is requested)
conn.commit()
conn.close()