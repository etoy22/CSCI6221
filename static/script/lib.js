function removeContent() {
    const selectedMovies = [];
    const checkboxes = document.getElementsByName('selected_movies[]');

    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            selectedMovies.push(checkboxes[i].value);
        }
    }

    fetch('/remove_movies', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ selectedMovies: selectedMovies })
    })
        .then(response => response.json())
        .then(data => {
            const success = data.success;
            console.log("Success:", success)
            if (!success) {
                window.alert('Removed Nothing');
            } else {
                window.location.href = "/library"
            }
        })
        .catch(error => console.error(error));
}
