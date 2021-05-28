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
        :param: Imagem capturada pelo OpenCv.
        :return: self.
        """
        # calculando o fps.
        self._current_time = time.time()
        fps = 1 / (self._current_time - self._previous_time)
        self._previous_time = self._current_time
        # exibindo fps
        cv.putText(img, f'FPS: {int(fps)}', self._position, cv.FONT_HERSHEY_PLAIN, 2, self._color, 3)

        return self


class Point:
    """ Classe para guardar posição de tela. """

    def __init__(self, x, y):
        self.y = y
        self.x = x

    def __str__(self):
        return f'Point(x={self.x}, y={self.y})'

    def __repr__(self):
        return f'<Point, x: {self.x}, y: {self.y}>'

    def __add__(self, other):
        """ Utilizando a adição entre objetos deste tipo. """
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """ Utilizando a subtração para objetos deste tipo. """
        return Point(self.x - other.x, self.y - other.y)

    def __iadd__(self, other):
        """ Utilizando a adição in-place. """
        self.x += other.x
        self.y += other.y
        return self

    def __cmp__(self, other):
        return self.x == other.x and self.y == other.y

    def as_tuple(self):
        """ Retorna o valor em tuplas. """
        return self.x, self.y
