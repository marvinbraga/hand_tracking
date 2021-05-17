# coding=utf-8
"""
Face Detect Basic Module.
"""
from core.abstract_middleware import BaseMiddleware
from core.face_detector import FaceDetector
from core.utils import FpsShowInfo
from core.video_capture import OpenCvVideoCapture


class FaceDetectorMiddleware(BaseMiddleware):
    """ Classe middleware para Face Detection. """

    def __init__(self, next_middleware=None):
        super().__init__(next_middleware=next_middleware)
        self._detector = FaceDetector(fps=FpsShowInfo(color=(0, 255, 9)))

    def _process(self, frame):
        """ Faz o processamento. """
        faces, frame = self._detector.find_faces(frame, show_face_info=True)
        print(faces)
        return frame


def main():
    """ Método de teste. """
    OpenCvVideoCapture(middleware=FaceDetectorMiddleware()).execute()


if __name__ == '__main__':
    main()
