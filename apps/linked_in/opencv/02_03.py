import cv2 as cv
import numpy as np

black = np.zeros([150, 200, 1], "uint8")
cv.imshow("Black", black)
print(black[0, 0, :])

ones = np.ones([150, 200, 3], "uint8")
cv.imshow("Ones", ones)
print(ones[0, 0, :])

white = np.ones([150, 200, 3], "uint16")
white *= 2**16 - 1
cv.imshow("Whites", white)
print(white[0, 0, :])

color = ones.copy()
color[:, :] = (255, 0, 0)
cv.imshow("Blue", color)
print(color[0, 0, :])

cv.waitKey(0)
cv.destroyAllWindows()
