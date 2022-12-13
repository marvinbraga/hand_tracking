"""
Face Mesh Detect Basic Module.
"""
from core.abstract_middleware import BaseMiddleware
from core.face_mesh_detector import FaceMeshDetector
from core.utils import FpsShowInfo
from core.video_capture import OpenCvVideoCapture


class FaceMeshMiddleware(BaseMiddleware):
    """Classe middleware para FaceMesh."""

    def __init__(self, next_middleware=None):
        super().__init__(next_middleware=next_middleware)
        self._detector = FaceMeshDetector(
            fps=FpsShowInfo(color=(90, 0, 0)),
            max_num_faces=3,
        )

    def _process(self, frame):
        """Faz o processamento."""
        frame, faces = self._detector.find_face_mesh(frame)
        if faces:
            print(faces[0])
        return frame


def main():
    """Método de teste."""
    OpenCvVideoCapture(middleware=FaceMeshMiddleware()).execute()


if __name__ == "__main__":
    main()
