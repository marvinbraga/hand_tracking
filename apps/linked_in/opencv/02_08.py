from core.abstract_middleware import BaseMiddleware
from core.video_capture import OpenCvVideoCapture


class SimpleCapture(BaseMiddleware):
    def _process(self, frame):
        return frame


def main():
    """Método de teste."""
    OpenCvVideoCapture(middleware=SimpleCapture(), win_name="Frame").execute()


if __name__ == "__main__":
    main()
