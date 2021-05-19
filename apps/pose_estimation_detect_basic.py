# coding=utf-8
"""
Pose Estimation Basic Module.
"""
from enum import Enum

import cv2 as cv
import numpy as np

from core.abstract_middleware import BaseMiddleware
from core.pose_estimation_detector import PoseEstimationDetector, PoseDetectorLandmark
from core.utils import FpsShowInfo
from core.video_capture import OpenCvVideoCapture


class MovStage(Enum):
    """ Classe para definir o estágio  """
    NONE = 0, ""
    DOWN = 1, "Baixo"
    UP = 2, "Cima"


class PoseCountAngleMiddleware(BaseMiddleware):
    """ Classe middleware para Face Detection. """

    _FONT = cv.FONT_HERSHEY_SIMPLEX

    def __init__(self, next_middleware=None):
        super().__init__(next_middleware=next_middleware)
        self._detector = PoseEstimationDetector(fps=FpsShowInfo(color=(0, 255, 0)))
        self._mov_stage = MovStage.NONE
        self._counter = 0

    def _calculate_angle(self, frame, ombro, cotovelo, punho, draw):
        """ Método para calcular entre o punho, cotovelo e ombro. """
        a = np.array(ombro)
        b = np.array(cotovelo)
        c = np.array(punho)

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        if draw:
            cv.putText(frame, str(angle), tuple(b.astype(int)),
                       self._FONT, 0.5, (255, 255, 255), 2, cv.LINE_AA)

        return angle, frame

    def _show_data(self, frame, angle):
        """ Exibir os dados relacionados aos movimentos. """
        if angle > 160:
            self._mov_stage = MovStage.DOWN
        if angle < 30 and self._mov_stage == MovStage.DOWN:
            self._mov_stage = MovStage.UP
            self._counter += 1

        cv.rectangle(frame, (0, 0), (225, 73), (245, 117, 16), -1)
        cv.putText(frame, 'NUM', (10, 15), self._FONT, 0.5, (0, 0, 0), 1, cv.LINE_AA)
        cv.putText(frame, str(self._counter), (10, 65), self._FONT, 1.5, (255, 255, 255), 2, cv.LINE_AA)
        cv.putText(frame, 'ESTAGIO', (95, 15), self._FONT, 0.5, (0, 0, 0), 1, cv.LINE_AA)
        cv.putText(frame, self._mov_stage.value[1], (90, 65), self._FONT, 1.5, (255, 255, 255), 2, cv.LINE_AA)

        return frame

    def _process(self, frame):
        """ Faz o processamento. """
        draw = True
        poses, frame = self._detector.find_pose(frame, draw)
        if poses:
            try:
                pose_ids = [
                    PoseDetectorLandmark.LEFT_SHOULDER.value,
                    PoseDetectorLandmark.LEFT_ELBOW.value,
                    PoseDetectorLandmark.LEFT_WRIST.value,
                ]
                self._detector.identify(frame, poses, pose_ids)
                angle, frame = self._calculate_angle(
                    frame,
                    poses[PoseDetectorLandmark.LEFT_SHOULDER.value][1],
                    poses[PoseDetectorLandmark.LEFT_ELBOW.value][1],
                    poses[PoseDetectorLandmark.LEFT_WRIST.value][1],
                    draw
                )
                frame = self._show_data(frame, angle)
            except Exception as e:
                print(e)

        return frame


def main():
    """ Método de teste. """
    OpenCvVideoCapture(middleware=PoseCountAngleMiddleware()).execute()


if __name__ == '__main__':
    main()
