import hashlib
import sqlite3


def addNewAccount(username,password):
    #Varriable to determine if a unique username went through
    passed = True

    #Connect to the database
    conn = sqlite3.connect('Databases/passwords.db')
    c = conn.cursor()

    # Hash the password for security
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Attempt to login
    try:
        c.execute('INSERT INTO users (username, hashed_password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()


        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        id = c.fetchone()
        conn.close()
        createNewLibrary(id)


    except sqlite3.IntegrityError:
        print("Error: Duplicate value for unique column")
        passed = False
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
    
    #Returns the id of the user if the username and password match, Returns false if username matches but password does
    if(passReturn==hashed_password):
        print("Username and Password Found")
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        return c.fetchone()
    else:
        return False

def createNewLibrary(accNum):
    conn = sqlite3.connect('Databases/accountLibrary.db')
    c = conn.cursor()
    movie_list=[]
    c.execute("INSERT INTO accounts (accNum, movie_list) VALUES (?, ?)", (accNum, str(movie_list)))
    conn.commit()
    conn.close()

def getMovies(accNum):
    conn = sqlite3.connect('Databases/accountLibrary.db')
    c = conn.cursor()

    c.execute("SELECT movie_list FROM accounts WHERE accNum = ?", (accNum,))

    rows = c.fetchall()

    movie_lists = []

    for row in rows:
        movie_list_str = row[0]
        movie_list = eval(movie_list_str)
        movie_lists.append(movie_list)

    conn.close()
    
    return movie_list

def addMovies(accNum,movieID):
    movie_list = getMovies(accNum)
    movie_list.append(movieID)
    movie_list_str = str(movie_list)

    conn = sqlite3.connect('Databases/accountLibrary.db')
    c = conn.cursor()
    c.execute("UPDATE accounts SET movie_list = ? WHERE accNum = ?", (movie_list_str,accNum))
    conn.commit()
    conn.close()



# print("admin passowrd")
# login("admin","password")
# print("---------\nadmin pass")
# login("admin","pass")
# print("---------\nad pass")
# login("ad","password")