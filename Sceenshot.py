from PIL import ImageGrab
from PIL import Image
from pynput import mouse
from pytesseract import pytesseract

path_to_tesseract = r"Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract
# define a callback function to be called when the left mouse button is clicked
def on_click(x, y, button, pressed):
    global x_pos, y_pos
    if button == mouse.Button.left and pressed:
        x_pos, y_pos = x,y
        # print the position of the mouse when the left button is clicked
        print(f"Left button clicked at ({x}, {y})")
        return False  # stop listening

x_pos, y_pos = None, None
x1,x2,y1,y2 = None,None,None,None
# create a listener for mouse events

with mouse.Listener(on_click=on_click) as listener:
    listener.join()
    x1,y1 = x_pos, y_pos

with mouse.Listener(on_click=on_click) as listener:
    listener.join()
    x2,y2 = x_pos, y_pos

# Double check the quardanates
print(f"Region: (left={x1}, top={y1}, right={x2}, bottom={y2}")

# Take quardanates and put them into the region that we will be using 
region = (x1, y1, x2, y2)

# Capture the specified region and save it as an image file called screenshot will override image if it already exists
image = ImageGrab.grab(bbox=region)
image.save("screenshot.png")

# Open image and then try to convert the image to text 
screen = Image.open("screenshot.png")
text = pytesseract.image_to_string(screen)
print(text[:-1])

# Tokenize the text into individual words
# words = nltk.word_tokenize(text)

# # Remove stop words (common words such as 'a', 'an', 'the', etc.)
# stop_words = set(nltk.corpus.stopwords.words('english'))
# filtered_words = [word.lower() for word in words if word.lower() not in stop_words]

# # Use the filtered words to determine the movie
# # You can define a dictionary of movie titles and their associated keywords
# movie_titles = {
#     'The Matrix': ['matrix', 'keanu', 'reeves', 'cyberpunk'],
#     'Jurassic Park': ['jurassic', 'dinosaur', 'island', 'jeff', 'goldblum']
# }

# # Loop through each movie and count the number of keywords that match the filtered words
# movie_matches = {}
# for movie, keywords in movie_titles.items():
#     matches = len(set(keywords).intersection(set(filtered_words)))
#     movie_matches[movie] = matches

# # Get the movie with the most keyword matches
# result = max(movie_matches, key=movie_matches.get)
# print('The movie is:', result)
