# coding=utf-8
"""
Módulo de Middleware Básico.
"""
import os.path
from abc import ABCMeta, abstractmethod

import cv2 as cv

from settings import BASE_DIR


class BaseMiddleware(metaclass=ABCMeta):
    """ Classe base para middleware. """
    def __init__(self, next_middleware=None):
        self._next = next_middleware

    @abstractmethod
    def _process(self, frame):
        pass

    def process(self, frame):
        """
        Método para processamento do middleware.
        :param frame:
        :return:
        """
        result = self._process(frame)
        if self._next:
            result = self._next.process(result)

        return result
