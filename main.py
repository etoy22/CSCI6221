from flask import Flask, render_template,request, jsonify
from account import addNewAccount, login
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('menu.html')

@app.route('/signup')
def signup():
    return render_template('signUp.html')

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
    print("Got here")
    username = request.form.get('username')
    password = request.form.get('password')

    # Do something with the form data
    print(username,password)
    success, id = login(username,password)
    
    return jsonify({'success': success,'id':id})


if __name__ == '__main__':
    app.run()