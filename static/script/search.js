/* 
search()
Takes the actor name and the movie name from the html and sends that result to the server
this ends up resulting in the displaying of the search values
 */
function search() {
    const movieName = document.getElementById('mName').value;
    const actorName = document.getElementById('aName').value;

    fetch('/searchMovies', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            movieName: movieName,
            actorName: actorName
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.success) {
                const moviesTableBody = document.querySelector('#movies-table tbody');
                moviesTableBody.innerHTML = '';
                data.movies.forEach(movie => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                <td><input type="checkbox" name="selected_movies[]" value="${movie.ID}"></td>
                <td>${movie.ID}</td>
                <td>${movie.Title}</td>
                <td>${movie.Release_Date}</td>
                <td>${movie.Overview}</td>
            `;
                    moviesTableBody.appendChild(tr);
                });
            } else {
                console.log('No search results found');
            }
        })
        .catch(error => console.error(error));
}
/* 
search()
Takes the an image from the user and sends that to the server
this ends up resulting in the displaying the text from the image as search results
 */
function search_Image() {

}


/* 
addToLibrary()
Takes the checkboxed values and gets the id's of those movies.
Sends those IDs to the server which adds them to the users library
 */
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
                window.alert('Nothing was selected');
            } else {
                window.alert('Added Movies');
            }
        })
        .catch(error => console.error(error));
}