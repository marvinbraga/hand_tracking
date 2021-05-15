# coding=utf-8
"""
Project Hand Tracking
"""
import time
from enum import Enum

import cv2 as cv
import mediapipe as mp


class HandLandMarks(Enum):
    """ Identificação de Land Marks. """
    WHIST = 0
    THUMB_CMC = 1
    THUMB_MCP = 2
    THUMB_IP = 3
    THUMB_TIP = 4
    INDEX_FINGER_MPC = 5
    INDEX_FINGER_PIP = 6
    INDEX_FINGER_DIP = 7
    INDEX_FINGER_TIP = 8
    MIDDLE_FINGER_MCP = 9
    MIDDLE_FINGER_PIP = 10
    MIDDLE_FINGER_DIP = 11
    MIDDLE_FINGER_TIP = 12
    RING_FINGER_MCP = 13
    RING_FINGER_PIP = 14
    RING_FINGER_DIP = 15
    RING_FINGER_TIP = 16
    PINK_MCP = 17
    PINK_PIP = 18
    PINK_DIP = 19
    PINK_TIP = 20


class FpsShowInfo:
    """ Classe para exibir a informação de Frames por Segundo. """

    def __init__(self, position=(10, 35), color=(255, 0, 255)):
        self._color = color
        self._position = position
        self._previous_time = time.time()
        self._current_time = time.time()

    def execute(self, img):
        """
        Método para exibir informação com OpenCv.
        :return: self.
        """
        # calculando o fps.
        self._current_time = time.time()
        fps = 1 / (self._current_time - self._previous_time)
        self._previous_time = self._current_time
        # exibindo fps
        cv.putText(img, f'FPS: {int(fps)}', self._position, cv.FONT_HERSHEY_PLAIN, 2, self._color, 3)

        return self


class HandPointsBold:
    """ Classe para enfatizar pontos das mãos. """

    def __init__(self, bold_points, draw=True, size=15, color=(255, 0, 255)):
        self._color = color
        self._size = size
        self._draw = draw
        self._bold_points = bold_points
        self._points = []

    @property
    def points(self):
        """ Retorna os pontos encontrados. """
        return self._points

    def show(self, image, hand_lms):
        """ Executa a presentação """
        self._points = []
        for nr_id, land_mark in enumerate(hand_lms.landmark):
            height, width, center = image.shape
            center_x, center_y = int(land_mark.x * width), int(land_mark.y * height)
            if HandLandMarks(nr_id) in self._bold_points:
                if self._draw:
                    cv.circle(image, (center_x, center_y), self._size, self._color, cv.FILLED)
                    self._points.append((nr_id, center_x, center_y))


class HandDetector:
    """ Classe para detecção de mãos. """

    def __init__(self, bold_points=None, fps=None, mode=False, max_hands=2, detection_con=0.5, track_con=0.5):
        self._bold_points = bold_points
        self._fps = fps
        self._points = []
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(mode, max_hands, detection_con, track_con)
        self.mp_draw = mp.solutions.drawing_utils

    @property
    def points(self):
        """ Retorna os pontos encontrados. """
        return self._points

    def find_hands(self, img, draw=True):
        """
        Método para procurar as mãos.
        :return: None
        """
        img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        self._fps.execute(img)

        self._points = []
        if results.multi_hand_landmarks:
            for hand_lms in results.multi_hand_landmarks:
                if self._bold_points:
                    self._bold_points.show(image=img, hand_lms=hand_lms)
                    self._points = self._bold_points.points
                if draw:
                    # Apresentando os pontos e os traços nas mãos.
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)

        return img


def main():
    """ Método de teste. """
    cap = cv.VideoCapture(0)
    detector = HandDetector(
        fps=FpsShowInfo(),
        bold_points=HandPointsBold(bold_points=[
            HandLandMarks.THUMB_TIP,
            HandLandMarks.INDEX_FINGER_TIP,
            HandLandMarks.MIDDLE_FINGER_TIP,
            HandLandMarks.RING_FINGER_TIP,
            HandLandMarks.PINK_TIP
        ])
    )
    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        print(detector.points)
        cv.imshow("Image", img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
