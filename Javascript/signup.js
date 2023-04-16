const signupForm = document.querySelector('#signup-form');
const signupButton = document.querySelector('#signUpButton');

signupButton.addEventListener('click', function (event) {
  const firstNameInput = document.querySelector('#first_name');
  console.log(document.querySelector('first_name'));
  console.log(document.querySelector('#first_name'));

  const lastNameInput = document.querySelector('#last_name');
  const emailInput = document.querySelector('#email');
  const usernameInput = document.querySelector('#username');
  const passwordInput = document.querySelector('#password');
  const confirmPasswordInput = document.querySelector('#ConfirmPassword');
  if (firstNameInput.checkValidity() && lastNameInput.checkValidity() && emailInput.checkValidity() && usernameInput.checkValidity() && passwordInput.checkValidity() && confirmPasswordInput.checkValidity()) {
    event.preventDefault();
    const formData = new FormData(signupForm);
    fetch('/newUser', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        const success = data.success;
        if (success) {
          window.alert('Signup successful!');
        } else {
          window.alert('Signup failed. Email or Username already in use.');
        }
      })
      .catch(error => {
        console.error(error);
      });
  }
});