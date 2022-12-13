import cv2
import numpy as np

img = cv2.imread("03_04.png")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
hsv_split = np.concatenate((h, s, v), axis=1)
cv2.imshow("Split HSV", hsv_split)

_, min_sat = cv2.threshold(s, 40, 255, cv2.THRESH_BINARY)
cv2.imshow("Sat Filter", min_sat)

_, max_hue = cv2.threshold(h, 15, 255, cv2.THRESH_BINARY_INV)
cv2.imshow("Hue Filter", max_hue)

final = cv2.bitwise_and(min_sat, max_hue)
cv2.imshow("Final", final)
cv2.imshow("Original", img)

cv2.waitKey(0)
cv2.destroyAllWindows()
