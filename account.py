import hashlib
import sqlite3


def addNewAccount(username,password):
    #Varriable to determine if a unique username went through
    passed = True

    #Connect to the database
    conn = sqlite3.connect('Databases/passwords.db')


    # Hash the password for security
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Attempt to login
    try:
        conn.execute('INSERT INTO users (username, hashed_password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: Duplicate value for unique column")
        passed = False

    # Close the database connection
    conn.close()
    return passed

def login(username,password):

    conn = sqlite3.connect('Databases/passwords.db')

    # Connect to the database
    c = conn.cursor()

    row = None
    # Execute the query to retrieve the password for the given username
    c.execute("SELECT hashed_password FROM users WHERE username = ?", (username,))
    row = c.fetchone()

    # Return None if User does not exist
    if row is None:
        print("User not found")
        return None
    
    passReturn = row[0]
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    #Returns True if the username and password match, Returns false if username matches but password does
    if(passReturn==hashed_password):
        print("Username and Password Found")
        return True
    else:
        return False
    
    
print("admin passowrd")
login("admin","password")
print("---------\nadmin pass")
login("admin","pass")
print("---------\nad pass")
login("ad","password")