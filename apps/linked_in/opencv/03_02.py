import cv2
import numpy as np

bw = cv2.imread("03_02.png", 0)
cv2.imshow("Original BW", bw)
h, w = bw.shape[0:2]

binary = np.zeros([h, w, 1], "uint8")

thresh = 85

# for row in range(h):
#     for col in range(w):
#         if bw[row][col] > thresh:
#             binary[row][col] = 255
#
# cv2.imshow("Slow Binary", binary)

ret, thresh = cv2.threshold(bw, thresh, 255, cv2.THRESH_BINARY)
cv2.imshow("CV Threshold", thresh)

cv2.waitKey(0)
cv2.destroyAllWindows()
