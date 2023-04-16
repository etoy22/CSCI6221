
function search() {

}

function addToLibrary() {
    const selectedMovies = [];
    const checkboxes = document.getElementsByName('selected_movies[]');

    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            selectedMovies.push(checkboxes[i].value);
        }
    }
    fetch('/add_movies', {
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
                window.alert('Added Nothing');
            } else {
                //Figure out where to go
                // window.location.href = "/search"
            }
        })
        .catch(error => console.error(error));
}
