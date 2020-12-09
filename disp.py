import cv2
from win32api import GetSystemMetrics

#the [x, y] for each right-click event will be stored here
right_clicks = list()

#this function will be called whenever the mouse is right-clicked
def mouse_callback(event, x, y, flags, params):

    #right-click event value is 2
    if event == 2:
        global right_clicks

        #store the coordinates of the right-click event
        right_clicks.append([x, y])

        print(right_clicks)

        cv2.destroyWindow('image')

img_l = cv2.imread("image0.jpg",0)
img_r = cv2.imread("image1.jpg",0)
scale_width = 1200 / img_l.shape[1]
scale_height = 800 / img_l.shape[0]
scale = min(scale_width, scale_height)
window_width = int(img_l.shape[1] * scale)
window_height = int(img_l.shape[0] * scale)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', window_width, window_height)

#set mouse callback function for window
cv2.setMouseCallback('image', mouse_callback)

cv2.imshow('image', img_l)
cv2.waitKey(0)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', window_width, window_height)
cv2.setMouseCallback('image', mouse_callback)

cv2.imshow('image', img_r)
cv2.waitKey(0)

cv2.destroyAllWindows()
