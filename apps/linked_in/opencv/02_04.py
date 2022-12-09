import cv2 as cv
import numpy as np

color = cv.imread("../../data/car.jpg")
cv.imshow("Image", color)
cv.moveWindow("Image", 0, 0)
print(color.shape)
height, width, channles = color.shape

b, g, r = cv.split(color)
rgb_split = np.empty([height, width * 3, 3], 'uint8')

rgb_split[:, 0:width] = cv.merge([b, b, b])
rgb_split[:, width: width * 2] = cv.merge([g, g, g])
rgb_split[:, width * 2:width * 3] = cv.merge([r, r, r])

cv.imshow("Channels", rgb_split)
cv.moveWindow("Channels", 0, height)

hsv = cv.cvtColor(color, cv.COLOR_BGR2HSV)
h, s, v = cv.split(hsv)
hsv_split = np.concatenate((h, s, v), axis=1)
cv.imshow("Split HSV", hsv_split)

cv.waitKey(0)
cv.destroyAllWindows()
