from flask import Flask, render_template, request, jsonify, redirect, session
import account as acc
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
    name = acc.getName(user_id)
    movies = acc.getMovies(user_id)
    mdetails = []
    for movie in movies:
        mdetails.append(searching.get_movie_details(movie))
    return render_template('library.html', name=name, movies=mdetails)


@app.route('/search')
def search():
    if 'sessionID' not in session:
        return redirect('/login')
    mdetails = []
    return render_template('search.html', movies=mdetails)


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
    success = acc.addNewAccount(
        first_name, last_name, email, username, password)
    return jsonify({'success': success})


@app.route('/loginUser', methods=['POST'])
def loginWeb():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Do something with the form data
        id = acc.login(username, password)
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


@app.route('/remove_movies', methods=['POST'])
def remove_movies():
    data = request.get_json()
    selected_movies = data['selectedMovies']
    if len(selected_movies) == 0:
        return jsonify({'success': False})

    user_id = session.get('user_id')

    acc.removeMovies(user_id, selected_movies)
    print("DONE")
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run()
