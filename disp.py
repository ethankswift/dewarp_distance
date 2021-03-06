import cv2
from win32api import GetSystemMetrics
import glob
import math

#the [x, y] for each click event will be stored here
clicks = []

images = glob.glob('measure\*.jpg')

# Defines the event that will be called when the mouse is clicked during point selection
def mouse_callback(event, x, y, flags, params):
    if event == 1:
        global clicks

        clicks.append([x, y])

        cv2.destroyWindow('image')

img_l = cv2.imread(images[0])
img_r = cv2.imread(images[1])

# Set parameters for window display so that it does not overfill the screen

scale_width = 1200 / img_l.shape[1]
scale_height = 800 / img_l.shape[0]
scale = min(scale_width, scale_height)
window_width = int(img_l.shape[1] * scale)
window_height = int(img_l.shape[0] * scale)

# Set window parameters and mouse callback function for window
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', window_width, window_height)
cv2.setMouseCallback('image', mouse_callback)

# Show first image
cv2.imshow('image', img_l)
cv2.waitKey(0)

# Reset window parameters and mouse callback function
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', window_width, window_height)
cv2.setMouseCallback('image', mouse_callback)

# Show second iamge
cv2.imshow('image', img_r)
cv2.waitKey(0)

# Using the pythagorean theorem to calculate the distance between points
pyth_result = math.sqrt( float( (clicks[0][0] - clicks[1][0]) ** 2 + (clicks[0][1] - clicks[1][1]) ** 2 ) )

print("My best guess is that this object is " + f'{(15374 * pyth_result ** -1.039):.2f}' + " inches away.")

cv2.destroyAllWindows()
