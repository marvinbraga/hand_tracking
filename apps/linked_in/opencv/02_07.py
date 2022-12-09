import cv2

img = cv2.imread('../../data/car.jpg')
cv2.imshow("Original", img)

# scale
half = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
stretch = cv2.resize(img, (600, 600))
stretch_near = cv2.resize(img, (600, 600), interpolation=cv2.INTER_NEAREST)

cv2.imshow("Half", half)
cv2.imshow("Stretch", stretch)
cv2.imshow("Streatch Near", stretch_near)

# Rotation
M = cv2.getRotationMatrix2D((0, 0), -30, 1)
rotated = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))
cv2.imshow("Rotated", rotated)

cv2.waitKey(0)
cv2.destroyAllWindows()
