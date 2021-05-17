# coding=utf-8
"""
Face Detector Module
"""
import cv2 as cv
import mediapipe as mp


class FaceDetector:
    """ Classe básica para detecção de faces. """

    def __init__(self, fps=None, min_detection_confidence=0.5, color=(0, 255, 0)):
        self._color = color
        self._fps = fps
        self._min_detection_confidence = min_detection_confidence
        # Face Detection
        self._mp_draw = mp.solutions.drawing_utils
        self._mp_face_detection = mp.solutions.face_detection
        self._face_detection = self._mp_face_detection.FaceDetection(min_detection_confidence=min_detection_confidence)

    @staticmethod
    def __get_bounding_box(frame, detection):
        """ Calcula a caixa de posicionamento da face. """
        image_h, image_w, image_c = frame.shape
        b_box_detected = detection.location_data.relative_bounding_box
        b_box = (int(b_box_detected.xmin * image_w), int(b_box_detected.ymin * image_h),
                 int(b_box_detected.width * image_w), int(b_box_detected.height * image_h))
        return b_box

    def _fancy_draw(self, frame, bounding_box, line_length=30, thickness=3, rectangle_length=1):
        x, y, w, h = bounding_box
        x1, y1 = x + w, y + h
        cv.rectangle(frame, bounding_box, self._color, rectangle_length)
        # Top Left
        cv.line(frame, (x, y), (x + line_length, y), self._color, thickness)
        cv.line(frame, (x, y), (x, y + line_length), self._color, thickness)
        # Top Right
        cv.line(frame, (x1, y), (x1 - line_length, y), self._color, thickness)
        cv.line(frame, (x1, y), (x1, y + line_length), self._color, thickness)
        # Bottom Left
        cv.line(frame, (x, y1), (x + line_length, y1), self._color, thickness)
        cv.line(frame, (x, y1), (x, y1 - line_length), self._color, thickness)
        # Bottom Right
        cv.line(frame, (x1, y1), (x1 - line_length, y1), self._color, thickness)
        cv.line(frame, (x1, y1), (x1, y1 - line_length), self._color, thickness)

        return frame

    def __draw_detection(self, frame, detection, show_face_info):
        """ Desenha a localização da face. """
        if show_face_info:
            b_box = self.__get_bounding_box(frame, detection)
            self._fancy_draw(frame, b_box)
            cv.putText(frame, f'{int(detection.score[0] * 100)}%', (b_box[0], b_box[1] - 10),
                       cv.FONT_HERSHEY_PLAIN, 1, self._color, 1)
        else:
            # Método padrão do MediaPipe.
            self._mp_draw.draw_detection(frame, detection)
        return frame

    def __get_face_info(self, frame, detect_id, detection):
        """ Recupera as informações dos pontos da face. """
        info = [detect_id, self.__get_bounding_box(frame, detection), detection.score]
        return info

    def find_faces(self, frame, draw=True, show_face_info=False):
        """ Procurar por faces """
        image_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = self._face_detection.process(image_rgb)
        faces = []
        if results.detections:
            for detect_id, detection in enumerate(results.detections):
                if draw:
                    self.__draw_detection(frame, detection, show_face_info)
                faces.append(self.__get_face_info(frame, detect_id, detection))

        if self._fps:
            self._fps.execute(frame)

        return faces, frame
