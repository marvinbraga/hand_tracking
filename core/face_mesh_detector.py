# coding=utf-8
"""
Face Mesh Detector Module
"""
import cv2 as cv
import mediapipe as mp


class FaceMeshDetector:
    """ Classe básica para detecção de pontos da face. """

    def __init__(self, fps=None, max_num_faces=1, static_image_mode=False, min_detection_confidence=0.5,
                 min_tracking_confidence=0.5, color=(0, 255, 0)):
        self._color = color
        self._fps = fps
        self._max_num_faces = max_num_faces
        self._min_tracking_confidence = min_tracking_confidence
        self._min_detection_confidence = min_detection_confidence
        self._static_image_mode = static_image_mode
        # Face Mesh
        self._mp_draw = mp.solutions.drawing_utils
        self._mp_face_mesh = mp.solutions.face_mesh
        self._face_mesh = self._mp_face_mesh.FaceMesh(max_num_faces=max_num_faces, static_image_mode=static_image_mode,
                                                      min_tracking_confidence=min_tracking_confidence,
                                                      min_detection_confidence=min_detection_confidence)
        self._draw_spec = self._mp_draw.DrawingSpec(thickness=1, circle_radius=2, color=color)

    def __draw_landmarks(self, frame, face_landmark):
        """ Exibe as marcas """
        self._mp_draw.draw_landmarks(
            frame, face_landmark, self._mp_face_mesh.FACE_CONNECTIONS, self._draw_spec, self._draw_spec)
        return frame

    def __get_face_points(self, frame, face_landmark, show_faces_points=False):
        """ Recupera as informações dos pontos da face. """
        face = []
        for lm_id, lm in enumerate(face_landmark.landmark):
            image_h, image_w, image_c = frame.shape
            x, y = int(lm.x * image_w), int(lm.y * image_h)
            if show_faces_points:
                cv.putText(frame, str(lm_id), (x, y), cv.FONT_HERSHEY_PLAIN, 0.7, self._color, 1)
            # print(lm_id, x, y)
            face.append([x, y])
        return face

    def find_face_mesh(self, frame, draw=True, show_faces_points=False):
        """ Método para processamento principal do middleware. """
        image_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = self._face_mesh.process(image_rgb)
        faces = []
        if results.multi_face_landmarks:
            for face_landmark in results.multi_face_landmarks:
                if draw:
                    self.__draw_landmarks(frame, face_landmark)
                faces.append(self.__get_face_points(frame, face_landmark, show_faces_points))

        if self._fps:
            self._fps.execute(frame)

        return frame, faces
