from PIL import Image
from pytesseract import pytesseract
import requests
import json
import searching

path_to_tesseract = r"Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract

# Open image and then try to convert the image to text 
screen = Image.open("screenshot.png")
text = pytesseract.image_to_string(screen)

lines = text.splitlines()

for line in lines:
    if line.strip():  # Check if the line is not empty
        searchTerms = (line)
        print(searchTerms)
        
        
    
for line in searchTerms:
    print(searching.movieSearch(line))
