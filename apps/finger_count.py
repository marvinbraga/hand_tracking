# coding=utf-8
"""
Project Finger Count
"""
import cv2 as cv
from hand_tracking import HandPointsBold, HandDetector
from apps.utils import FpsShowInfo
from apps.hand_land_marks import HandLandMarks

# Cria o HandDetector.
detector = HandDetector(
    fps=FpsShowInfo(color=(90, 90, 90)),
    bold_points=HandPointsBold(bold_points=[
        HandLandMarks.INDEX_FINGER_MPC,
        HandLandMarks.THUMB_TIP,
        HandLandMarks.INDEX_FINGER_PIP,
        HandLandMarks.INDEX_FINGER_TIP,
        HandLandMarks.MIDDLE_FINGER_PIP,
        HandLandMarks.MIDDLE_FINGER_TIP,
        HandLandMarks.RING_FINGER_PIP,
        HandLandMarks.RING_FINGER_TIP,
        HandLandMarks.PINK_PIP,
        HandLandMarks.PINK_TIP
    ])
)

# Inicializa o OpenCV.
cap = cv.VideoCapture(0)
cam_height, cam_width = 640, 480
cap.set(3, cam_width)
cap.set(4, cam_height)

while True:
    success, img = cap.read()
    img = detector.find_hands(img)
    # Se recuperou a posição dos dedos.
    landmarks = detector.points
    if landmarks:
        # Thumb
        fingers = []
        if landmarks[0][2] < landmarks[1][2]:
            fingers.append(1)
        else:
            fingers.append(0)
        # Outros dedos
        for index in range(2, 10, 2):
            if landmarks[index + 1][2] < landmarks[index][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        total_fingers = fingers.count(1)
        print(total_fingers, fingers)

    cv.imshow("Image", img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
