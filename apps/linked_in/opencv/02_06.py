import cv2
import numpy as np

image = cv2.imread("../../data/car.jpg")
cv2.imshow("Original", image)

blur = cv2.GaussianBlur(image, (5, 55), 0)
cv2.imshow("Blur", blur)

kernel = np.ones((5, 5), "uint8")
dilate = cv2.dilate(image, kernel, iterations=1)
erode = cv2.erode(image, kernel, iterations=1)

cv2.imshow("Dilate", dilate)
cv2.imshow("Erode", erode)

cv2.waitKey(0)
cv2.destroyAllWindows()
