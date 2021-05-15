import math

import cv2 as cv
import numpy


class RangeFingers:
    """ Classe para controlar a diferença entre dois dedos. """
    box_width, box_height = 150, 400

    def __init__(self, detector, min_length, max_length, value_range, color=(255, 0, 255)):
        self._value_range = value_range
        self._min_value, self._max_value = value_range[0], value_range[1]
        self._color = color
        self._max_length = max_length
        self._min_length = min_length
        self._detector = detector
        self._length = 0
        self._box_tax = self._value = 0
        self._box_value = self.box_height

    @property
    def length(self):
        """
        Retorna a distância entre os dedos
        :return: int
        """
        return self._length

    @property
    def value(self):
        """
        Recupera o valor da diferença entre os dedos
        :return:
        """
        return self._value

    def _create_line(self, img, x1, y1, x2, y2, draw=True):
        """
        Exibe a linha e o ponto central
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :return:
        """
        self._length = math.hypot(x2 - x1, y2 - y1)
        if draw:
            # círculo do meio da linha
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            # Criando a linha.
            cv.line(img, (x1, y1), (x2, y2), self._color, 3)
            cv.circle(img, (cx, cy), 12, self._color, cv.FILLED)

            # Pinta o círculo de acordo com o tamanho.
            if self._length <= self._min_length:
                cv.circle(img, (cx, cy), 12, (0, 255, 0), cv.FILLED)
            elif self._length >= self._max_length:
                cv.circle(img, (cx, cy), 12, (0, 0, 255), cv.FILLED)

    def process(self, img, draw=True):
        """
        Calcula o tamanho e exibe
        :param img: Imagem do cv.
        :param draw: Se é para exibir a informação sobre o percentual do tamanho.
        :return:
        """
        land_marks = self._detector.points
        if land_marks:
            x1, y1 = land_marks[0][1], land_marks[0][2]
            x2, y2 = land_marks[1][1], land_marks[1][2]
            # Recuperando o tamanho da linha
            self._create_line(img, x1, y1, x2, y2, draw)
            # Ajusta o volume de acordo com os valores registrados.
            self._value = numpy.interp(self._length, [self._min_length, self._max_length],
                                       [self._min_value, self._max_value])
            self._box_value = numpy.interp(self._length, [self._min_length, self._max_length],
                                           [self.box_height, self.box_width])
            self._box_tax = numpy.interp(self._length, [self._min_length, self._max_length], [0, 100])

        return self

    def show(self, img, color):
        """
        Exibe o range.
        :return:
        """
        cv.rectangle(img, (50, 150), (85, 400), color, 3)
        cv.rectangle(img, (50, int(self._box_value)), (85, 400), color, cv.FILLED)
        cv.putText(img, f'{int(self._box_tax)}%', (50, 425), cv.FONT_HERSHEY_COMPLEX, 0.75, color, 3)
        return img
