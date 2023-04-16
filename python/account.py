import hashlib
import sqlite3

'''
addNewAccount()
Creates a new account with the details given
'''
def addNewAccount(first_name, last_name, email, username, password):
    # Varriable to determine if a unique username went through
    passed = True

    # Connect to the database
    conn = sqlite3.connect('Databases/data.db')
    c = conn.cursor()

    # Hash the password for security
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Attempt to login
    try:
        c.execute('INSERT INTO users (fname, lname, email, username, hashed_password) VALUES (?, ?, ?, ?, ?)',
                  (first_name, last_name, email, username, hashed_password))
        conn.commit()
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        id = c.fetchone()
        conn.close()
        createNewLibrary(id[0])

    except sqlite3.IntegrityError:
        passed = False
        conn.close()

    return passed

'''
createNewLibrary()
Creates a new library when one creates a new account
'''
def createNewLibrary(accNum):
    conn = sqlite3.connect('Databases/data.db')
    c = conn.cursor()
    movie_list = []
    c.execute("INSERT INTO accounts (accNum, movie_list) VALUES (?, ?)",
              (accNum, str(movie_list)))
    conn.commit()
    conn.close()


'''
login()
Allows the user to login
'''
def login(username, password):
    conn = sqlite3.connect('Databases/data.db')
    c = conn.cursor()
    row = None

    # Execute the query to retrieve the password for the given username
    c.execute(
        "SELECT hashed_password, id FROM users WHERE username = ?", (username,))
    row = c.fetchone()

    # Return None if User does not exist
    if row is None:
        conn.close()
        return None

    hashed_password, user_id = row
    if hashed_password == hashlib.sha256(password.encode()).hexdigest():
        conn.close()
        return user_id
    else:
        conn.close()
        return None

'''
getName()
Given a users_id get the name of the individual
'''

def getName(id):
    conn = sqlite3.connect('Databases/data.db')
    c = conn.cursor()

    c.execute("SELECT fName FROM users WHERE id = ?", (id,))
    result = c.fetchall()

    conn.close()
    return result[0][0]

'''
getMovies()
Given a users_id get the library that the users have seen
'''
def getMovies(accNum):
    conn = sqlite3.connect('Databases/data.db')
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

'''
addMovies()
Given a users_id and the movie_id add the movies to the users library
'''
def addMovies(accNum, movieIDs):
    movie_list = []
    movie_list.extend(getMovies(accNum))
    for id in movieIDs:
        if id not in movie_list:
            movie_list.append(int(id))
    movie_list.sort()
    movie_list_str = str(movie_list)

    conn = sqlite3.connect('Databases/data.db')
    c = conn.cursor()
    c.execute("UPDATE accounts SET movie_list = ? WHERE accNum = ?",
              (movie_list_str, accNum))
    conn.commit()
    conn.close()

'''
removeMovies()
Given a users_id and the movie_id remove the movies from the users library
'''
def removeMovies(accNum, movieIDs):
    movie_list = []
    movie_list.extend(getMovies(accNum))
    for id in movieIDs:
        movie_list.remove(int(id))

    movie_list_str = str(movie_list)

    conn = sqlite3.connect('Databases/data.db')
    c = conn.cursor()
    c.execute("UPDATE accounts SET movie_list = ? WHERE accNum = ?",
              (movie_list_str, accNum))
    conn.commit()
    conn.close()
