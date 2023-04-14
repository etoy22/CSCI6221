from flask import Flask, render_template, request, jsonify, redirect, session
from account import addNewAccount, login, getName,getMovies
import searching
import secrets
import uuid

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route('/')
def index():
    return render_template('menu.html')

@app.route('/signup')
def signup():
    return render_template('signUp.html')

@app.route('/library')
def library():
    if 'sessionID' not in session:
        return redirect('/login')
    user_id = session.get('user_id')
    name = getName(user_id)
    movies = getMovies(user_id)
    mdetails = []
    for movie in movies:
        mdetails.append(searching.get_movie_details(movie))
    print(mdetails)
    return render_template('library.html',name=name,movies=mdetails)

@app.route('/search')
def search():
    if 'sessionID' not in session:
        return redirect('/login')
    return render_template('search.html')

@app.route('/login')
def loginAccount():
    return render_template('login.html')

@app.route('/newUser', methods=['POST'])
def signupWeb():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    confirmedpassword = request.form.get('ConfirmPassword')

    # Do something with the form data
    print(first_name,last_name,email,username,password,confirmedpassword)
    success = addNewAccount(first_name,last_name,email,username,password)
    return jsonify({'success': success})


@app.route('/loginUser', methods=['POST'])
def loginWeb():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Do something with the form data
        id = login(username, password)
        if id is not None:

            session['sessionID'] = uuid.uuid4().hex
            session['user_id'] = id
            return jsonify({'success': True})
            # return redirect('/library')
        else:
            print("Invalid username or password")
            return jsonify({'success': False})
    else:
        return redirect("/library")
    



if __name__ == '__main__':
    app.run()