import sys  #for cmd line arguments
import sqlite3  #for database
import re #email,password validation
import random
import array
#https://www.sqlite.org/whentouse.html
#https://www.tutorialspoint.com/sqlite/sqlite_python.htm
#https://linuxhint.com/install_sqlite_browser_ubuntu_1804/#:~:text=First%20open%20the%20SQLite%20database,database%20to%20your%20desired%20format.
#login for multiple users 
#password generator

def menu():
	print('***************  Usage: ***************')
	print('  1) main.py new - To create new password   ')
	print('  2) main.py <website> - To get the password')
	print('  3) main.py email <website> - To get the email')
	print('  4) main.py edit <website> - To edit the password')
	print('  5) main.py delete <website> - To delete the password')
	
def check_email(email):
 
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False
        
def check_pass(password):
 
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$'
    if(re.fullmatch(regex, password)):
        return True
    else:
        return False


def password_gen():
	MAX_LEN = 12

	DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
					'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
					'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
					'z']

	UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
					'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
					'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
					'Z']

	SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
		'*', '(', ')', '<']

	COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS


	rand_digit = random.choice(DIGITS)
	rand_upper = random.choice(UPCASE_CHARACTERS)
	rand_lower = random.choice(LOCASE_CHARACTERS)
	rand_symbol = random.choice(SYMBOLS)

# at this stage, the password contains only 4 characters but
# we want a 12-character password
	temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol


# now that we are sure we have at least one character from each
# set of characters, we fill the rest of
# the password length by selecting randomly from the combined
# list of character above.
	for x in range(MAX_LEN - 4):
		temp_pass = temp_pass + random.choice(COMBINED_LIST)

	# convert temporary password into array and shuffle to
	# prevent it from having a consistent pattern
	# where the beginning of the password is predictable
		temp_pass_list = array.array('u', temp_pass)
		random.shuffle(temp_pass_list)


	password = ""
	for x in temp_pass_list:
		password = password + x
		
	return password

def create_table():
	conn = sqlite3.connect('database.db')
	statement = '''CREATE TABLE if not exists Manager
	(Id INTEGER PRIMARY KEY AUTOINCREMENT,
	Website TEXT NOT NULL,
	Password TEXT NOT NULL,
	Email TEXT NOT NULL
	);
	'''
	cur = conn.cursor()
	cur.execute(statement)
	conn.close()

	


def create_new_password():
	conn = sqlite3.connect('database.db')
	statement = '''INSERT INTO Manager(Website,Password,Email)
	VALUES(?,?,?)
	'''
	website = input('Enter Website name: ')
	
	permission = input('Do you want me to generate a password for you? yes or no : ')
	
	if(permission == 'yes'):
		password = password_gen()
	else:
		password = input(f'Enter Password for {website}: ')
		if check_pass(password) == False:
			print(f'{password} is not strong')
			cont = input('Do you still want to continue? yes or no : ')
			if cont=='no':
	         		print('Record is not created.Please try again')
	         		return 
	email = input(f'Enter Email associated with {website}: ')
	if check_email(email) == False:
		print(f'{email} is not valid email')
		print('Record is not created.Please try again')
		return 
	cur = conn.cursor()
	cur.execute(statement,(website,password,email))
	
	conn.commit()
	conn.close()
	print(f'Password for {website} succesfully recorded!')
	




def get_password(website):
	conn = sqlite3.connect('database.db')
	statement = '''SELECT Password FROM Manager where Website = ?
	'''
	
	cur = conn.cursor()
	items = cur.execute(statement,(website,))
	#column after website to know that it is tuple
	item = items.fetchone()
	if item is None:
		print(f'No record found for {website}')
	else:
		#item = [i for i in items]
		print(f'password for {website} is {item[0]} ')
	
	conn.close()

def get_email(website):
	conn = sqlite3.connect('database.db')
	statement = '''SELECT Email FROM Manager where Website = ?
	'''
	
	cur = conn.cursor()
	items = cur.execute(statement,(website,))
	#column after website to know that it is tuple
	item = items.fetchone()
	if item is None:
		print(f'No record found for {website}')
	else:
		#item = [i for i in items]
		print(f'Email for {website} is {item[0]} ')
	
	conn.close()
	
def edit_password(website):
	conn = sqlite3.connect('database.db')
	statement = '''UPDATE Manager set Password = ? where Website = ?
	'''
	newp = input('Enter new password :  ')
	cur = conn.cursor()
	cur.execute(statement,(newp,website,))
	print(f'Password for {website} is updated')
	conn.commit()
	conn.close()

def delete_password(website):
	conn = sqlite3.connect('database.db')
	statement = '''DELETE FROM Manager where Website = ?
	'''
	cur = conn.cursor()
	cur.execute(statement,(website,))
	print(f'Record for {website} is deleted')
	conn.commit()
	conn.close()
	


if len(sys.argv) == 2:
	if sys.argv[1] == 'new':
		create_table()
		create_new_password()
	else:
		get_password(sys.argv[1])
elif len(sys.argv) > 2:
	if sys.argv[1] == 'email':
		get_email(sys.argv[2])
	elif sys.argv[1] == 'edit':
		edit_password(sys.argv[2])
	elif sys.argv[1] == 'delete':
		delete_password(sys.argv[2])
else:
	menu()
		






