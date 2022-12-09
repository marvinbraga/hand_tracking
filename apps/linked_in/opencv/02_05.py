import cv2 as cv
import numpy as np

color = cv.imread("../../data/car.jpg", 1)

gray = cv.cvtColor(color, cv.COLOR_RGB2GRAY)
cv.imwrite("gray.jpg", gray)

b = color[:, :, 0]
g = color[:, :, 1]
r = color[:, :, 2]

rgba = cv.merge((b, g, r, g))
cv.imwrite("rgba.png", rgba)
