const loginForm = document.querySelector('#login-form');
const loginButton = document.querySelector('#loginButton');

loginButton.addEventListener('click', function (event) {
    event.preventDefault();
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
});