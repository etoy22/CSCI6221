/* 
login()
Takes the username and password sends it to the server to check if they are correct
If correct sends the user to their library
 */

function login() {

    const loginForm = document.querySelector('#login-form');
    const loginButton = document.querySelector('#loginButton');


    const formData = new FormData(loginForm);
    fetch('/loginUser', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            const success = data.success;
            if (!success) {
                window.alert('Login failed. Username or password is wrong.');
            } else {
                window.location.href = "/library"
            }
        })
        .catch(error => {
            console.error(error);
        });
}