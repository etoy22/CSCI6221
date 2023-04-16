from flask import Flask, render_template, request, jsonify, redirect, session
import account as acc
import searching as ser
import secrets
import uuid

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

'''
Functions for the Menu page
First is route | Function         | Purpose 
/              | index()          | Serves as the Main menu page
'''


@app.route('/')
def index():
    return render_template('menu.html')


'''
Functions for the Sign Up page
First is route | Function         | Purpose 
/signup        | signup()         | Serves as the Sign Up page
/newUser       | signupWeb()      | Allows for the implementation and creation of new users
'''


@app.route('/signup')
def signup():
    return render_template('signUp.html')


@app.route('/newUser', methods=['POST'])
def signupWeb():
    fName = request.form.get('first_name')
    lName = request.form.get('last_name')
    email = request.form.get('email')
    user = request.form.get('username')
    password = request.form.get('password')
    success = acc.addNewAccount(
        fName, lName, email, user, password)
    return jsonify({'success': success})


'''
Functions for the Login page
First is route | Function         | Purpose 
/login         | loginAccount()   | Serves as the Login page
/loginUser     | loginWeb()       | Serves to check if the account actually exists and if it does login to the account

'''


@app.route('/login')
def loginAccount():
    return render_template('login.html')


@app.route('/loginUser', methods=['POST'])
def loginWeb():
    username = request.form.get('username')
    password = request.form.get('password')

    id = acc.login(username, password)
    if id is not None:
        # Creates a session for the users and ties their user id to the session
        session['sessionID'] = uuid.uuid4().hex
        session['user_id'] = id
        return jsonify({'success': True})
    else:
        # Gets here if the account doesn't exist
        print("Invalid username or password")
        return jsonify({'success': False})


'''
Functions for the Library page
First is route | Function         | Purpose 
/library       | library()        | Serves as the Library page and has a record of all the movies a user has watched
/remove_movies | remove_movies()  | 
'''


@app.route('/library')
def library():
    if 'sessionID' not in session:
        return redirect('/login')
    user_id = session.get('user_id')
    name = acc.getName(user_id)
    movies = acc.getMovies(user_id)
    mdetails = []
    for movie in movies:
        mdetails.append(ser.get_movie_details(movie))
    return render_template('library.html', name=name, movies=mdetails)

@app.route('/remove_movies', methods=['POST'])
def remove_movies():
    if 'sessionID' not in session:
        return redirect('/login')
    data = request.get_json()
    selMovies = data['selectedMovies']
    if len(selMovies) == 0:
        return jsonify({'success': False})

    user_id = session.get('user_id')

    acc.removeMovies(user_id, selMovies)
    print("DONE")
    return jsonify({'success': True})


'''
Functions for the Search page
First is route | Function         | Purpose 
/search        | search()         | Serves as the 
/searchMovies  | searchMovies()   | 
/add_movies    | addMoviesImage() |
'''

@app.route('/search', methods=['GET'])
def search():
    if 'sessionID' not in session:
        return redirect('/login')
    return render_template('search.html', movies=[])


@app.route('/searchMovies', methods=['GET','POST'])
def searchMovies():
    if 'sessionID' not in session:
        return redirect('/login')
    data = request.get_json()
    movieSearch = data['movieName']
    actorSearch = data['actorName']

    mdetails = []
    if (movieSearch == "" and actorSearch == ""):
        return jsonify({'success': False})
    elif (movieSearch == ""):
        mdetails = ser.actorSearch(actorSearch)
    elif (actorSearch ==""):
        mdetails = ser.movieSearch(movieSearch)
    else:
        mdetails = ser.actorMovieSearch(actorSearch,movieSearch)
    print(mdetails)
    return jsonify({'success': True, 'movies':mdetails})

@app.route('/add_movies', methods=['POST'])
def addMovies():
    if 'sessionID' not in session:
        return redirect('/login')
    print('temp')

@app.route('/add_movies_image', methods=['POST'])
def addMoviesImage():
    if 'sessionID' not in session:
        return redirect('/login')
    print('temp')


if __name__ == '__main__':
    app.run(debug=True)
