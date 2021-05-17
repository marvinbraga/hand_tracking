# coding=utf-8
"""
Módulo de OpenCvVideoCapture.
"""
import os
from enum import Enum

import cv2 as cv


class OpenCvFlip(Enum):
    """ Configurações para flip de imagem. """
    HORIZONTAL = 0,
    VERTICAL = 1,
    BOTH = -1


class OpenCvVideoCapture:
    """ Classe para trabalhar com o OpenCvVideoCapture. """

    def __init__(self, middleware, flip=OpenCvFlip.VERTICAL, cam_height=640, cam_width=480,
                 file_name=None,
                 win_name='OpenCV Video Capture | Frame', *args, **kwargs):
        self._file_name = file_name
        self._win_name = win_name
        self._flip = flip
        self._args = args
        self._kwargs = kwargs
        self._middleware = middleware
        self._cap = self.init_capture()
        self._cap.set(3, cam_width)
        self._cap.set(4, cam_height)

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
        while True:
            ret, img = self._cap.read()
            img = cv.flip(img, self._flip.value[0])
            if self._middleware:
                self._middleware.process(img)

            cv.imshow(self._win_name, img)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        cv.destroyAllWindows()
