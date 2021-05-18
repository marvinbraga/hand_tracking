# coding=utf-8
"""
Utils Module.
"""
import time

import cv2 as cv


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