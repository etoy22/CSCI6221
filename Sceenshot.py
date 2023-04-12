from pynput import mouse
from PIL import ImageGrab

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

