import numpy as np
import cv2 as cv
import glob

# Termination criteria for the cornerSubPix function
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Initializng the data structure we will use to contain point data
objp = np.zeros((7*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)

print("7x7 object matrix intialized...")

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# Unix style pathname expanstion to grab all of the calibration images and put them in an array
images = glob.glob('calibrate\*.jpg')

print("Loading " + str(len(images)) + " for calibration from calibrate directory...")

for fname in images:
    print("Examining: " + fname)
    img = cv.imread(fname)

    # Set parameters for window display so that it does not overfill the screen
    scale_width = 1200 / img.shape[1]
    scale_height = 800 / img.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(img.shape[1] * scale)
    window_height = int(img.shape[0] * scale)
    cv.namedWindow('image', cv.WINDOW_NORMAL)
    cv.resizeWindow('image', window_width, window_height)

    # Convert loaded image to greyscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    retval, corners = cv.findChessboardCorners(gray, (7,7), None)
    # If found, add object points, image points (after refining them)
    if retval == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv.drawChessboardCorners(img, (7,7), corners2, retval)
        cv.imshow('image', img)
        cv.waitKey(10)
    else:
        print("Finding corners on " + fname + " failed!")

print("Creating camera calibration matrix...")

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

img = cv.imread(images[6])
h,  w = img.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

# undistort
dst = cv.undistort(img, mtx, dist, None, newcameramtx)
# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.imshow('image', img)
cv.waitKey(0)
cv.imshow('image', dst)
cv.waitKey(0)

cv.destroyAllWindows()
