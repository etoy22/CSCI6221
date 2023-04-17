from PIL import Image
from pytesseract import pytesseract
import requests
import json
import os

'''API key'''
api_key = '03645002b465428658913956c71ee9e7'

'''
get_movie_details
Given a movies id recieve details about the movie
'''


def get_movie_details(movie_id):
    api_key = '03645002b465428658913956c71ee9e7'
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}')

    movie = response.json()
    over = movie['overview'][:100]+"..."
    return {
        'ID': movie['id'],
        'Title': movie['title'],
        'Release_Date': movie['release_date'],
        'Overview': over
    }


'''
movieSearch()
Given a Title search for a movie
'''


def movieSearch(movie_query):

    list = []
    # Search by movie
    api_key = '03645002b465428658913956c71ee9e7'
    response = requests.get(
        f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_query}')

    # Parse the JSON response
    search_results = json.loads(response.text)
    for result in search_results['results']:
        if len(result['overview']) > 100:
            over = result['overview'][:100]+"..."
        else:
            over = result['overview']
        my_dict = {}
        my_dict['ID'] = result['id']
        my_dict['Title'] = result['title']
        my_dict['Release_Date'] = result['release_date']
        my_dict['Overview'] = over
        list.append(my_dict)
    return list


'''
actorSearch()
Given a Actor search for a movie
'''


def actorSearch(actor_name):
    list = []
    # Make a GET request to the TMDb API search endpoint to get the actor's ID
    response = requests.get(
        f'https://api.themoviedb.org/3/search/person?api_key={api_key}&query={actor_name}')
    search_results = json.loads(response.text)

    # Search through all actors with the name
    for actor_id in search_results['results']:
        # Make a GET request to the TMDb API discover endpoint to get the movies that the actor has starred in
        response = requests.get(
            f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_cast={actor_id}')
        discover_results = json.loads(response.text)

        for result in discover_results['results']:
            if len(result['overview']) > 100:
                over = result['overview'][:100]+"..."
            else:
                over = result['overview']
            my_dict = {}
            my_dict['ID'] = result['id']
            my_dict['Title'] = result['title']
            try:
                my_dict['Release_Date'] = result['release_date']
            except:
                pass
            my_dict['Overview'] = over
            list.append(my_dict)
    return list


'''
actorMovieSearch()
Given an Actor and a Movie Title search for a movie
'''


def actorMovieSearch(actor_name, movie_title):
    list = []
    # Make a GET request to the TMDb API search endpoint to get the actor's ID
    response = requests.get(
        f'https://api.themoviedb.org/3/search/person?api_key={api_key}&query={actor_name}')
    search_results = json.loads(response.text)

    # Get the first actor's ID from the search results
    for id in search_results['results']:
        actor_id = id['id']

        # Make a GET request to the TMDb API discover endpoint to get the movies that the actor has starred in
        response = requests.get(
            f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_cast={actor_id}')
        discover_results = json.loads(response.text)

        # Filter the movie results by searching for the movie title
        for result in discover_results['results']:
            if movie_title.lower() in result['title'].lower():
                if len(result['overview']) > 100:
                    over = result['overview'][:100]+"..."
                else:
                    over = result['overview']

                my_dict = {}
                my_dict['ID'] = result['id']
                my_dict['Title'] = result['title']
                try:
                    my_dict['Release_Date'] = result['release_date']
                except:
                    my_dict['Release_Date'] = "N/A"
                my_dict['Overview'] = over
                list.append(my_dict)
        return list


'''
imageSearch()
Given an image search for a movie
'''


def imageSearch(img):
    # Download at https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.0.20221222.exe
    path_to_tesseract = r"Tesseract-OCR\tesseract.exe"
    pytesseract.tesseract_cmd = path_to_tesseract

    # Open image and then try to convert the image to text
    screen = Image.open(img)
    text = pytesseract.image_to_string(screen)

    lines = text.splitlines()
    searchTerms = []
    for line in lines:
        if line.strip():  # Check if the line is not empty
            searchTerms.append(line)

    value = []
    for search in searchTerms:
        hold = (movieSearch(search))
        if len(hold) != 0:
            value.extend(hold)

    return value
