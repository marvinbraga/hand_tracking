# coding=utf-8
"""
Módulo de OpenCvVideoCapture.
"""
from enum import Enum

import cv2 as cv


class OpenCvFlip(Enum):
    """ Configurações para flip de imagem. """
    HORIZONTAL = 0,
    VERTICAL = 1,
    BOTH = -1


class OpenCvVideoCapture:
    """ Classe para trabalhar com o OpenCvVideoCapture. """

    def __init__(self, middleware, flip=OpenCvFlip.VERTICAL, *args, **kwargs):
        self._flip = flip
        self._args = args
        self._kwargs = kwargs
        self._middleware = middleware
        self._cap = cv.VideoCapture(0)

    def execute(self):
        """
        Método para executa o OpenCvVideoCapture
        :return:
        """
        while True:
            ret, img = self._cap.read()
            img = cv.flip(img, self._flip.value[0])
            self._middleware.process(img)

            cv.imshow('frame', img)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        cv.destroyAllWindows()
