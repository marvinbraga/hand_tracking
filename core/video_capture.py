# coding=utf-8
"""
Módulo de OpenCvVideoCapture.
"""
import os
from enum import Enum

import cv2 as cv


class OpenCvFlip(Enum):
    """ Configurações para flip de imagem. """
    HORIZONTAL = 0
    VERTICAL = 1
    BOTH = -1


class OpenCvScreen:
    """ Classe para definir as configurações do screen. """

    def __init__(self, width=640, height=480):
        self._height = height
        self._width = width

    @property
    def width(self):
        """ Retornar a largura. """
        return self._width

    @property
    def height(self):
        """ Retorna a altura. """
        return self._height


class OpenCvVideoCapture:
    """ Classe para trabalhar com o OpenCvVideoCapture. """

    def __init__(self, middleware, flip=OpenCvFlip.VERTICAL, screen=OpenCvScreen(),
                 file_name=None,
                 win_name='OpenCV Video Capture | Frame', *args, **kwargs):
        self._screen = screen
        self._file_name = file_name
        self._win_name = win_name
        self._flip = flip
        self._args = args
        self._kwargs = kwargs
        self._middleware = middleware
        self._cap = self.init_capture()
        self._cap.set(3, screen.width)
        self._cap.set(4, screen.height)

    @property
    def screen(self):
        """ Retorna informações do screen. """
        return self._screen

    def init_capture(self):
        """ Inicializa a captura de vídeo. """
        if self._file_name:
            result = cv.VideoCapture(os.path.normpath(self._file_name))
        else:
            result = cv.VideoCapture(0)
        return result

    def execute(self):
        """
        Método para executa o OpenCvVideoCapture
        :return:
        """
        while self._cap.isOpened():
            ret, frame = self._cap.read()
            frame = cv.flip(frame, self._flip.value)
            if self._middleware:
                self._middleware.process(frame)

            cv.imshow(self._win_name, frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        self._cap.release()
        cv.destroyAllWindows()
