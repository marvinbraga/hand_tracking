"""
Pose Estimation Tracking
"""
from enum import Enum

import cv2 as cv
import mediapipe as mp


class PoseDetectorLandmark(Enum):
    """Classe para inversão de dependencia do PoseLandmark."""

    NOSE = 0
    LEFT_EYE_INNER = 1
    LEFT_EYE = 2
    LEFT_EYE_OUTER = 3
    RIGHT_EYE_INNER = 4
    RIGHT_EYE = 5
    RIGHT_EYE_OUTER = 6
    LEFT_EAR = 7
    RIGHT_EAR = 8
    MOUTH_LEFT = 9
    MOUTH_RIGHT = 10
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14
    LEFT_WRIST = 15
    RIGHT_WRIST = 16
    LEFT_PINKY = 17
    RIGHT_PINKY = 18
    LEFT_INDEX = 19
    RIGHT_INDEX = 20
    LEFT_THUMB = 21
    RIGHT_THUMB = 22
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_KNEE = 25
    RIGHT_KNEE = 26
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28
    LEFT_HEEL = 29
    RIGHT_HEEL = 30
    LEFT_FOOT_INDEX = 31
    RIGHT_FOOT_INDEX = 32


class PoseEstimationDetector:
    """Classe para detectar movimentos do corpo humano."""

    def __init__(
        self,
        fps=None,
        static_image_mode=False,
        upper_body_only=False,
        smooth_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        color=(0, 255, 0),
        point_color=(255, 0, 255),
    ):
        self._point_color = point_color
        self._color = color
        self._min_tracking_confidence = min_tracking_confidence
        self._min_detection_confidence = min_detection_confidence
        self._smooth_landmarks = smooth_landmarks
        self._upper_body_only = upper_body_only
        self._static_image_mode = static_image_mode
        self._fps = fps
        self._mp_draw = mp.solutions.drawing_utils
        self._mp_pose = mp.solutions.pose
        self._pose = self._mp_pose.Pose(
            static_image_mode=static_image_mode,
            # model_complexity=upper_body_only,
            smooth_landmarks=smooth_landmarks,
            # enable_segmentation=min_detection_confidence,
            smooth_segmentation=min_tracking_confidence,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def _get_pose_points(self, frame, landmark, draw):
        """Recupera as informações dos pontos do corpo."""
        image_h, image_w, image_c = frame.shape
        cx, cy = int(landmark.x * image_w), int(landmark.y * image_h)
        if draw:
            cv.circle(frame, (cx, cy), 5, self._point_color, cv.FILLED)
        pose = [cx, cy]
        return pose

    def identify(self, frame, poses, pose_ids: list, size=15):
        """Salienta o ponto do id informado."""
        for i in pose_ids:
            cv.circle(
                frame,
                (poses[i][1][0], poses[i][1][1]),
                size,
                self._point_color,
                cv.FILLED,
            )
        return self

    def find_pose(self, frame, draw=True):
        """Procura pelo corpo humano."""
        image_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = self._pose.process(image_rgb)
        poses = []
        if results.pose_landmarks:
            for pose_id, landmark in enumerate(results.pose_landmarks.landmark):
                if draw:
                    self._mp_draw.draw_landmarks(
                        image=frame,
                        landmark_list=results.pose_landmarks,
                        connections=self._mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=self._mp_draw.DrawingSpec(
                            color=self._point_color,
                            thickness=1,
                            circle_radius=1,
                        ),
                        connection_drawing_spec=self._mp_draw.DrawingSpec(
                            color=self._color,
                            thickness=2,
                            circle_radius=2,
                        ),
                    )
                poses.append([pose_id, self._get_pose_points(frame, landmark, draw)])

        if self._fps:
            self._fps.execute(frame)

        return poses, frame
