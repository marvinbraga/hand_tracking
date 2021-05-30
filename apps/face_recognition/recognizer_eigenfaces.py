# coding=utf-8
"""
Módulo de Reconhecedor EigenFaces.
"""
import os

import cv2 as cv

import settings
from apps.face_recognition.capture import FaceDetectHaarcascade
from core.abstract_middleware import BaseMiddleware
from core.utils import RecognizerType
from core.video_capture import OpenCvVideoCapture, NamedBox


class Faces2Recognize:
    """ Classe que contem informações sobre as faces que deverão ser detectadas. """
    @staticmethod
    def get_name(value):
        """ Recupera o nome da pessoa reconhecida pelo Id. """
        result = {
            1: 'Marcus Vinicius Braga',
            2: 'Giovanna da Fonte',
            3: 'João da Fonte',
            4: 'Andréa da Fonte'
        }.get(value)
        return result


class EigenFaceRecognizer(BaseMiddleware):
    """ Reconhecedor EigenFace. """
    _width, _height = 220, 220

    def __init__(self, next_middleware=None):
        super(EigenFaceRecognizer, self).__init__(next_middleware)
        self._recognizer_type = RecognizerType.EIGEN
        self._recognizer = self._recognizer_type.new_recognizer(num_components=50, threshold=2)
        self._recognizer.read(
            os.path.join(settings.BASE_DIR + '/data/training', f'{self._recognizer_type.value[1]}.yml'))
        self._faces = []
        self._gray_image = None

    def add_faces(self, value):
        """ Informa as faces detectadas. """
        self._faces = []
        self._faces.append(value)
        return self

    def set_gray_image(self, value):
        """ Informa a imagem cinza. """
        self._gray_image = value
        return self

    def _process(self, frame):
        """ Executa o processo de reconhecimento. """
        for x, y, w, h in self._faces:
            print(len(self._faces))
            image = cv.resize(self._gray_image[y: y + h, x: x + w], (self._width, self._height))
            image_id, assurance = self._recognizer.predict(image)
            NamedBox(frame, Faces2Recognize.get_name(image_id), (x, y)).show()
            cv.putText(frame, f'{assurance}', (x, y - 10), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
        return frame


def main():
    """ Método de teste. """
    OpenCvVideoCapture(
        middleware=FaceDetectHaarcascade(
            next_middleware=EigenFaceRecognizer()
        )
    ).execute()


if __name__ == '__main__':
    main()
