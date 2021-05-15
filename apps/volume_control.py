# coding=utf-8
"""
Project Volume Control
"""
from ctypes import cast, POINTER

import cv2 as cv
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from hand_tracking import HandPointsBold, HandDetector
from apps.utils import FpsShowInfo
from apps.hand_land_marks import HandLandMarks
from range_fingers import RangeFingers

# Ativa os controles de áudio.
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Cria o HandDetector.
detector = HandDetector(
    fps=FpsShowInfo(color=(90, 90, 90)),
    bold_points=HandPointsBold(bold_points=[
        HandLandMarks.THUMB_TIP,
        HandLandMarks.INDEX_FINGER_TIP
    ])
)

# Recupera o valores de máximo e mínimos de volume.
vol_range = volume.GetVolumeRange()
MIN_LENGTH, MAX_LENGTH = 15, 194
# Ativa o comando de distância entre dedos
volume_range_control = RangeFingers(detector, MIN_LENGTH, MAX_LENGTH, vol_range, color=(255, 0, 255))

# Inicializa o OpenCV.
cap = cv.VideoCapture(0)
cam_height, cam_width = 640, 480
cap.set(3, cam_width)
cap.set(4, cam_height)

while True:
    success, img = cap.read()
    img = detector.find_hands(img)
    # Se recuperou a posição dos dedos.
    if detector.points:
        # Recupera o volume ajustado de acordo com a distância entre dedos e seu range.
        vol = volume_range_control.process(img).value
        # Ajusta o volume
        volume.SetMasterVolumeLevel(vol, None)
    # imprime a caixa visualizadora de volume
    img = volume_range_control.show(img, (0, 255, 0))

    cv.imshow("Image", img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
