# coding=utf-8
"""
Módulo de OpenCvVideoCapture.
"""
import os
from abc import ABCMeta, abstractmethod
from enum import Enum

import cv2 as cv
import numpy as np

from core.utils import Point, GetScreen


class OpenCvFlip(Enum):
    """ Configurações para flip de imagem. """
    NONE = 9
    HORIZONTAL = 0
    VERTICAL = 1
    BOTH = -1


class NamedBox:
    """ Classe para apresentar uma caixa de texto para nomes. """

    def __init__(self, frame, name, position, text_color=(255, 255, 255), line_color=(255, 255, 255),
                 back_color=(90, 0, 0)):
        self._position = Point(*position)
        self._frame = frame
        self._back_color = back_color
        self._line_color = line_color
        self._text_color = text_color
        self._name = name
        if not name:
            self._name = 'DESCONHECIDO'
            self._back_color = (0, 0, 125)

    def _paint_box(self, start, end, text):
        """ Pinta a caixa de texto e o texto. """
        cv.rectangle(self._frame, start.as_tuple(), end.as_tuple(), self._back_color, -1)
        cv.rectangle(self._frame, start.as_tuple(), end.as_tuple(), self._line_color, 2)
        cv.putText(self._frame, self._name, text.as_tuple(), cv.FONT_HERSHEY_DUPLEX, 0.5, self._text_color, 1,
                   cv.LINE_AA)
        return self

    def _paint_indicator_box(self, start, end):
        """ Pinta o indicador da caixa. """
        point_1 = Point(start.x + 10, end.y)
        point_2 = Point(point_1.x + 10, point_1.y)
        point_3 = Point(self._position.x + 50, self._position.y - 70)
        triangle = np.array([point_1.as_tuple(), point_2.as_tuple(), point_3.as_tuple()])
        cv.drawContours(self._frame, [triangle], 0, self._back_color, -1)
        cv.drawContours(self._frame, [triangle], 0, self._line_color, 2)
        return self

    def show(self):
        """ Método para exibir a caixa de texto. """
        text_size = cv.getTextSize(self._name, cv.FONT_HERSHEY_DUPLEX, 0.5, 1)
        text_width, text_height = text_size[0]
        start_point = Point(self._position.x - 20, self._position.y - 150)
        end_point = Point(start_point.x + text_width + 18, start_point.y + text_height + 20)
        text_point = Point(start_point.x + 10, start_point.y + 22)
        self._paint_box(start_point, end_point, text_point)._paint_indicator_box(start_point, end_point)
        return self


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

    def as_tuple(self):
        """ Retorna tupla com valores. """
        return self._width, self._height


class AbstractOpenCvVideoCapture(metaclass=ABCMeta):
    """ Classe para trabalhar com o OpenCvVideoCapture. """
    cap = None

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

    @abstractmethod
    def init_capture(self):
        """ Inicializa a captura de vídeo. """
        pass

    def execute(self):
        """
        Método para executa o OpenCvVideoCapture
        :return:
        """
        while self._cap.isOpened():
            ret, frame = self._cap.read()
            if self._flip is not OpenCvFlip.NONE:
                frame = cv.flip(frame, self._flip.value)
            if self._middleware:
                frame = self._middleware.process(frame)

            cv.imshow(self._win_name, frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            elif cv.waitKey(1) & 0xFF == ord('s'):
                self._middleware.save_image()

        self._cap.release()
        cv.destroyAllWindows()


class OpenCvVideoCapture(AbstractOpenCvVideoCapture):
    """ Classe para trabalhar com o OpenCvVideoCapture. """

    def init_capture(self):
        """ Inicializa a captura de vídeo. """
        if self._file_name:
            if self._file_name == "screen":
                result = GetScreen()
            else:
                result = cv.VideoCapture(os.path.normpath(self._file_name))
        else:
            result = cv.VideoCapture(0)
        if OpenCvVideoCapture.cap:
            result = OpenCvVideoCapture.cap
        else:
            OpenCvVideoCapture.cap = result
        return result


class OpenCvCamCaptureByRtsp(AbstractOpenCvVideoCapture):
    
    def __init__(self, username, password, ip, port, rote,
                 middleware=None,
                 flip=OpenCvFlip.VERTICAL,
                 screen=OpenCvScreen(),
                 win_name='OpenCV Video Capture | Frame',
                 *args, **kwargs):
        # /cam/realmonitor?channel=1&subtype=0
        self._url = f'rtsp://{username}:{password}@{ip}:{port}{rote}'
        super().__init__(middleware, flip, screen, win_name=win_name, *args, **kwargs)

    def init_capture(self):
        os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'
        result = cv.VideoCapture(self._url, cv.CAP_FFMPEG)
        return result


class OpenCvCanvas:
    
    def __init__(self, middleware=None, win_name="Canvas"):
        self._win_name = win_name
        self._middleware = middleware
        self._canvas = None
        self._init_canvas()

    def _init_canvas(self):
        self._canvas = np.ones([500, 500, 3], "uint8") * 255
        return self

    def execute(self):
        while True:
            frame = self._canvas
            if self._middleware:
                frame = self._middleware.process(frame)

            cv.imshow(self._win_name, frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            elif cv.waitKey(1) & 0xFF == ord('s'):
                self._middleware.save_image()

        cv.destroyAllWindows()
