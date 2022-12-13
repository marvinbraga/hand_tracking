import cv2 as cv

img = cv.imread("../../data/car.jpg")
cv.namedWindow("Image", cv.WINDOW_NORMAL)
cv.imshow("Image", img)
cv.waitKey(0)
