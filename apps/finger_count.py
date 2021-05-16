# coding=utf-8
"""
Project Finger Count
"""

from core.hand_land_marks import HandLandMarks
from core.abstract_middleware import BaseMiddleware
from core.utils import FpsShowInfo
from core.video_capture import OpenCvVideoCapture
from core.hand_tracking import HandPointsBold, HandDetector


class FingerCountMiddleware(BaseMiddleware):
    """ Verificação da contagem de dedos que não estão recolhidos. """

    def __init__(self, next_middleware=None):
        super().__init__(next_middleware=next_middleware)
        # Cria o HandDetector.
        self._detector = HandDetector(
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

    def _process(self, frame):
        """ Executa o processamento da contagem. """
        self._detector.find_hands(frame)
        # Se recuperou a posição dos dedos.
        landmarks = self._detector.points
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


def main():
    """ Método de teste. """
    OpenCvVideoCapture(middleware=FingerCountMiddleware()).execute()


if __name__ == '__main__':
    main()
