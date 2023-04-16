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

function search_Image() {

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
                window.alert('Nothing was selected');
            } else {
                window.alert('Added Movies');
            }
        })
        .catch(error => console.error(error));
}