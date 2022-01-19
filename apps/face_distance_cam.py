# coding=utf-8
"""
Face Distance of Cam
"""
import cv2

from core.abstract_middleware import BaseMiddleware
from core.face_mesh_detector import FaceMeshDetector
from core.utils import FpsShowInfo
from core.video_capture import OpenCvVideoCapture


class FaceDistanceOfCam(BaseMiddleware):
    """
    Classe de Middleware para medir a distância entre uma face e a câmera.
    """

    def __init__(self, next_middleware=None):
        super().__init__(next_middleware=next_middleware)
        self._detector = FaceMeshDetector(fps=FpsShowInfo(color=(90, 0, 0)), max_num_faces=1)

    def _process(self, frame):
        frame, faces = self._detector.find_face_mesh(frame, draw=False)
        if faces:
            face = faces[0][1]
            point_left = face[145]
            point_right = face[374]
            cv2.line(frame, point_left, point_right, (0, 200, 0), 3)
            cv2.circle(frame, point_left, 5, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, point_right, 5, (255, 0, 255), cv2.FILLED)
            w = self._detector.find_distance(point_left, point_right)

            # Finding the focal length
            W = 6.3
            # d = 50
            f = 375.9  # (w * d) / W

            # Finding the distance
            d = (W * f) / w
            print(d)

        return frame


def main():
    """ Método de teste. """
    OpenCvVideoCapture(middleware=FaceDistanceOfCam()).execute()


if __name__ == '__main__':
    main()
