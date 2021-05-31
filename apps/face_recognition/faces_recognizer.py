# coding=utf-8
"""
Módulo de Reconhecedor Genérico de Faces.
"""
import os

import cv2 as cv

import settings
from apps.face_recognition.capture import FaceDetectHaarcascade
from core.abstract_middleware import BaseMiddleware
from core.utils import RecognizerType
from core.video_capture import OpenCvVideoCapture, NamedBox, OpenCvScreen


class Faces2Recognize:
    """ Classe que contem informações sobre as faces que deverão ser detectadas. """

    @staticmethod
    def get_name(value):
        """ Recupera o nome da pessoa reconhecida pelo Id. """
        result = {
            1: 'Marcus Vinicius Braga',
            2: 'Giovanna da Fonte',
            3: 'Joao da Fonte',
            4: 'Andrea da Fonte'
        }.get(value)
        return result


class FaceRecognizer(BaseMiddleware):
    """ Reconhecedor EigenFace. """
    _width, _height = 220, 220

    def __init__(self, next_middleware=None,
                 recognizer_type=RecognizerType.LBPH, recognizer_params={}, color=(0, 255, 0)):
        super(FaceRecognizer, self).__init__(next_middleware)
        self._color = color
        self._recognizer_type = recognizer_type
        self._recognizer = self._recognizer_type.new_recognizer(**recognizer_params)
        self._recognizer.read(
            os.path.join(settings.BASE_DIR + '/data/training', f'{self._recognizer_type.value[1]}.yml'))
        self._faces = []
        self._gray_image = None

    def clear_faces(self):
        """ Inicializa o array de faces. """
        self._faces = []
        return self

    def add_faces(self, value):
        """ Informa as faces detectadas. """
        self._faces.append(value)
        return self

    def set_gray_image(self, value):
        """ Informa a imagem cinza. """
        self._gray_image = value
        return self

    def _process(self, frame):
        """ Executa o processo de reconhecimento. """
        for x, y, w, h in self._faces:
            image = cv.resize(self._gray_image[y: y + h, x: x + w], (self._width, self._height))
            image_id, assurance = self._recognizer.predict(image)
            cv.putText(frame, f'{int(assurance)}', (x, y - 10), cv.FONT_HERSHEY_PLAIN, 1, self._color, 1)
            cv.putText(
                frame, f'{self._recognizer_type.value[1]}', (x, y + h + 10),
                cv.FONT_HERSHEY_PLAIN, 0.5, self._color, 1)
            if assurance < 20:
                NamedBox(frame, Faces2Recognize.get_name(image_id), (x, y + 20)).show()
        return frame


def main():
    """ Método de teste. """
    OpenCvVideoCapture(
        # file_name='screen', screen=OpenCvScreen(1200, 800),
        middleware=FaceDetectHaarcascade(
            next_middleware=FaceRecognizer()
        )
    ).execute()


if __name__ == '__main__':
    main()
