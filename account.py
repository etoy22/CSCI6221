import hashlib
import sqlite3


def addNewAccount(first_name,last_name,email,username,password):
    #Varriable to determine if a unique username went through
    passed = True

    #Connect to the database
    conn = sqlite3.connect('Databases/passwords.db')
    c = conn.cursor()

    # Hash the password for security
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Attempt to login
    try:
        c.execute('INSERT INTO users (fname, lname, email, username, hashed_password) VALUES (?, ?, ?, ?, ?)', (first_name,last_name,email,username, hashed_password))
        conn.commit()
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        id = c.fetchone()
        print(id[0])
        conn.close()
        createNewLibrary(id[0])


    except sqlite3.IntegrityError:
        print("Error: Duplicate value for unique column")
        passed = False
        conn.close()

    return passed

def login(username, password):
    conn = sqlite3.connect('Databases/passwords.db')
    c = conn.cursor()
    row = None
    
    # Execute the query to retrieve the password for the given username
    c.execute("SELECT hashed_password, id FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    
    # Return None if User does not exist
    if row is None:
        print("User not found")
        conn.close()
        return None
    
    hashed_password, user_id = row
    if hashed_password == hashlib.sha256(password.encode()).hexdigest():
        print("Username and Password Found")
        conn.close()
        return user_id
    else:
        conn.close()
        return None


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


addMovies(1,278)


# print("admin passowrd")
# login("admin","password")
# print("---------\nadmin pass")
# login("admin","pass")
# print("---------\nad pass")
# login("ad","password")