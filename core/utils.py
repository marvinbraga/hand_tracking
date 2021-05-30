# coding=utf-8
"""
Utils Module.
"""
import os
import time

import cv2 as cv
import cv2.data as cv_data

import numpy as np
from PIL import ImageGrab
from enum import Enum


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


class FancyDraw:
    """ Pinta quadrado de indicação. """

    def __init__(self, color=(0, 255, 0), line_length=30, thickness=3, rectangle_length=1):
        self._color = color
        self._rectangle_length = rectangle_length
        self._thickness = thickness
        self._line_length = line_length

    def paint(self, frame, bounding_box):
        """ Executa a pintura do quadrado. """
        x, y, w, h = bounding_box
        x1, y1 = x + w, y + h
        cv.rectangle(frame, bounding_box, self._color, self._rectangle_length)
        # Top Left
        cv.line(frame, (x, y), (x + self._line_length, y), self._color, self._thickness)
        cv.line(frame, (x, y), (x, y + self._line_length), self._color, self._thickness)
        # Top Right
        cv.line(frame, (x1, y), (x1 - self._line_length, y), self._color, self._thickness)
        cv.line(frame, (x1, y), (x1, y + self._line_length), self._color, self._thickness)
        # Bottom Left
        cv.line(frame, (x, y1), (x + self._line_length, y1), self._color, self._thickness)
        cv.line(frame, (x, y1), (x, y1 - self._line_length), self._color, self._thickness)
        # Bottom Right
        cv.line(frame, (x1, y1), (x1 - self._line_length, y1), self._color, self._thickness)
        cv.line(frame, (x1, y1), (x1, y1 - self._line_length), self._color, self._thickness)
        return frame


class GetScreen:
    """ Classe para pegar o screen do computador. """

    def __init__(self, top=0, left=0, bottom=800, right=600):
        self._top = top
        self._left = left
        self._bottom = bottom
        self._right = right

    def set(self, pos_id, value):
        """ Altera as configurações do screen. """
        if pos_id == 1:
            self._top = value
        elif pos_id == 2:
            self._left = value
        elif pos_id == 3:
            self._bottom = value
        elif pos_id == 4:
            self._right = value
        return self

    def isOpened(self):
        """ Informa que está funcionando. """
        return True

    def read(self):
        """ Recupera a imagem da tela """
        b_box = (self._top, self._left, self._bottom, self._right)
        print_screen = np.array(ImageGrab.grab(bbox=b_box))
        return b_box, print_screen

    def release(self):
        """ Não precisa retornar nada. """
        pass


class HaarcascadesFiles:
    """ Classe para recupera os arquivos haarcascades instalados. """

    @staticmethod
    def get(value):
        """ Recupera o caminho completo do arquivo de acordo com o valor informado. """
        files = {f.split('.')[0]: os.path.join(cv_data.haarcascades, f) for f in os.listdir(cv_data.haarcascades)}
        return files.get(value)


class RecognizerType(Enum):
    """ Tipos de reconhecedores. """
    EIGEN = 0, 'EigenFace'
    FISHER = 1, 'FisherFace'
    LBPH = 2, 'LBPHFace'

    def new_recognizer(self, *args, **kwargs):
        """ Factory Method para Recognizer. """
        result = {
            RecognizerType.EIGEN: cv.face.EigenFaceRecognizer_create,
            RecognizerType.FISHER: cv.face.FisherFaceRecognizer_create,
            RecognizerType.LBPH: cv.face.LBPHFaceRecognizer_create
        }[self]
        return result(*args, **kwargs)
