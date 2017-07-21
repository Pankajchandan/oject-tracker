import numpy as np
import cv2

# Load an color image in grayscale
img = cv2.imread('/home/pankaj/Downloads/home.jpg',0)
WINDOW_NAME = 'Image'
cv2.namedWindow(WINDOW_NAME)
cv2.startWindowThread()

# Display an image
cv2.imshow(WINDOW_NAME,img)
cv2.waitKey(0) 


cv2.destroyWindow(WINDOW_NAME)
