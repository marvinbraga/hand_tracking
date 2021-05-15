# coding=utf-8
"""
Finger Detect Module.
"""
from core.hand_tracking import HandDetector, HandPointsBold
from core.abstract_middleware import BaseMiddleware
from core.utils import FpsShowInfo
from core.video_capture import OpenCvVideoCapture


class FingerDetectMiddleware(BaseMiddleware):
    """ Testa todos os pontos das mãos. """

    def __init__(self, next_middleware=None):
        super().__init__(next_middleware=next_middleware)
        self._detector = HandDetector(fps=FpsShowInfo(), bold_points=HandPointsBold(bold_points='__all__'))

    def _process(self, frame):
        """ Método para exibir pontos das mãos. """
        frame = self._detector.find_hands(frame)
        print(self._detector.points)
        return frame


def main():
    """ Método de teste. """
    OpenCvVideoCapture(middleware=FingerDetectMiddleware()).execute()


if __name__ == '__main__':
    main()
