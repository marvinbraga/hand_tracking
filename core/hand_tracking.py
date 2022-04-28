# coding=utf-8
"""
Project Hand Tracking
"""

import cv2 as cv
import mediapipe as mp

from core.hand_land_marks import HandLandMarks


class HandPointsBold:
    """ Classe para enfatizar pontos das mãos. """

    def __init__(self, bold_points, draw=True, size=15, color=(255, 0, 255)):
        self._color = color
        self._size = size
        self._draw = draw
        self._bold_points = bold_points
        if bold_points == '__all__':
            self._bold_points = HandLandMarks.all()
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
                    self._bold_points.prepare(image=img, hand_lms=hand_lms)
                    self._points = self._bold_points.points
                if draw:
                    # Apresentando os pontos e os traços nas mãos.
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)

        return img
