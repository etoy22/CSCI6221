import requests
import json

# Replace YOUR_API_KEY with your TMDb API key
api_key = '03645002b465428658913956c71ee9e7'



def movieSearch(movie_query):
    # Search by movie
    response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_query}')

    # Parse the JSON response
    search_results = json.loads(response.text)

    print("-------")
    print("Movie Info that is being used")
    # Print the search results id
    for result in search_results['results']:
        print("ID:", result['id'],end=" ")
        print("Title:", result['title'],end=" ")
        print("Release Date:", result['release_date'],end=" ")
        print("Overview:", result['overview'])
        print("----------")

def actorSearch(actor_name):
    # Make a GET request to the TMDb API search endpoint to get the actor's ID
    response = requests.get(f'https://api.themoviedb.org/3/search/person?api_key={api_key}&query={actor_name}')
    search_results = json.loads(response.text)

    # Search through all actors with the name
    for actor_id in search_results ['results']:
        # Make a GET request to the TMDb API discover endpoint to get the movies that the actor has starred in
        response = requests.get(f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_cast={actor_id}')
        discover_results = json.loads(response.text)

        print("Example to analysis")
        print(discover_results['results'])


        for result in discover_results['results']:
            print("ID:", result['id'],end=" ")
            print("Title:", result['title'],end=" ")
            try:
                print("Release Date:", result['release_date'],end=" ")
            except:
                pass
            print("Overview:", result['overview'])
            print("----------")

def actorMovieSearch(actor_name,movie_title):
    # Make a GET request to the TMDb API search endpoint to get the actor's ID
    response = requests.get(f'https://api.themoviedb.org/3/search/person?api_key={api_key}&query={actor_name}')
    search_results = json.loads(response.text)

    # Get the first actor's ID from the search results
    for id in search_results ['results']:
        actor_id = id['id']

        # Make a GET request to the TMDb API discover endpoint to get the movies that the actor has starred in
        response = requests.get(f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_cast={actor_id}')
        discover_results = json.loads(response.text)

        # Filter the movie results by searching for the movie title
        for result in discover_results['results']:
            if movie_title.lower() in result['title'].lower():
                print("ID:", result['id'],end=" ")
                print("Title:", result['title'],end=" ")
                try:
                    print("Release Date:", result['release_date'],end=" ")
                except:
                    pass
                print("Overview:", result['overview'])
                print("----------")

# print("Movie Search")
# movieSearch("matrix")
# print("Actor Search")
# actorSearch("keanu")
print("Movie and Actor Search")
actorMovieSearch("keanu","matrix")