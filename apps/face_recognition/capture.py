# coding=utf-8
"""
Face Capture
"""
import os

import cv2 as cv

from core.abstract_middleware import BaseMiddleware
from core.utils import FancyDraw
from core.video_capture import OpenCvVideoCapture
from settings import BASE_DIR


class LimitReached(Exception):
    """ Exceção para limite alcançado. """

    def __init__(self):
        super(LimitReached, self).__init__('Limite de capturas alcançado.')


class FaceDetectHaarcascade(BaseMiddleware):
    """ Classe para Captura de Face com Haarcascade. """

    def __init__(self, next_middleware=None, color=(0, 255, 0)):
        super(FaceDetectHaarcascade, self).__init__(next_middleware)
        self._color = color
        self._classfier = self.get_cascade('haarcascade_frontalface_default.xml')
        self._eye_classfier = self.get_cascade('haarcascade_eye.xml')

    def _process(self, frame):
        """ Executa o processamento da captura de face. """
        gray_image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = self._classfier.detectMultiScale(
            gray_image, scaleFactor=1.5, minSize=(100, 100))
        # Pinta o quadrado.
        for x, y, w, h in faces:
            b_box = x, y, w, h
            frame = FancyDraw(self._color).paint(frame, b_box)
            if self._next and isinstance(self._next, FaceCaptureHaarcascade):
                self._next.add_faces(b_box)
                self._next.set_gray_image(gray_image)
            break

        return frame


class FaceCaptureHaarcascade(BaseMiddleware):
    """ Classe para fazer a captura de faces com o Haarcascade. """
    _width, _height = 220, 220

    def __init__(self, next_middleware=None):
        super(FaceCaptureHaarcascade, self).__init__(next_middleware)
        self._id = int(input('Informe o identificador numérico da face: '))
        print('Pressione ENTER para bater um foto para o treinamento.')
        self._max = 25
        self._order = 1
        self._faces = []
        self._gray_image = None

    def add_faces(self, value):
        """ Informa as faces detectadas. """
        self._faces.append(value)
        return self

    def set_gray_image(self, value):
        """ Informa a imagem cinza. """
        self._gray_image = value
        return self

    def _save_captured_image(self):
        return os.path.join(BASE_DIR, f'data/photos/face_{self._id}_{self._order}.jpg')

    def _process(self, frame):
        """ Executa a captura da imagem. """
        if self._faces:
            for x, y, w, h in self._faces:
                # Salva a imagem.
                if cv.waitKey(1) & 0xFF == 13:
                    image = cv.resize(self._gray_image[y: y + h, x: x + w], (self._width, self._height))
                    file_name = self._save_captured_image()
                    cv.imwrite(file_name, image)
                    print(file_name, 'capturada com sucesso.')
                    self._order += 1
                if self._order >= self._max + 1:
                    raise LimitReached()
                break
        return frame


def main():
    """ Método de teste. """
    try:
        OpenCvVideoCapture(
            middleware=FaceDetectHaarcascade(
                next_middleware=FaceCaptureHaarcascade())
        ).execute()
    except LimitReached as e:
        print(e)


if __name__ == '__main__':
    main()
