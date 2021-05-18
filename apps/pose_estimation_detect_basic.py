# coding=utf-8
"""
Pose Estimation Basic Module.
"""
from core.abstract_middleware import BaseMiddleware
from core.pose_estimation_detector import PoseEstimationDetector
from core.utils import FpsShowInfo
from core.video_capture import OpenCvVideoCapture


class PoseEstimationDetectorMiddleware(BaseMiddleware):
    """ Classe middleware para Face Detection. """

    def __init__(self, next_middleware=None):
        super().__init__(next_middleware=next_middleware)
        self._detector = PoseEstimationDetector(fps=FpsShowInfo(color=(0, 255, 0)))

    def _process(self, frame):
        """ Faz o processamento. """
        poses, frame = self._detector.find_pose(frame)
        if poses:
            pose_ids = [0, 1, 4]
            self._detector.identify(frame, poses, pose_ids)
            for i in pose_ids:
                print(poses[i])
        return frame


def main():
    """ Método de teste. """
    OpenCvVideoCapture(middleware=PoseEstimationDetectorMiddleware()).execute()


if __name__ == '__main__':
    main()
