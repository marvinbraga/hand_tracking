import cv2

from core.abstract_middleware import BaseMiddleware
from core.video_capture import OpenCvVideoCapture


class SimpleCapture(BaseMiddleware):
    point = (0, 0)
    radius = 100
    line_width = 3
    color = (0, 255, 0)
    passed, setted = False, False

    def click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print("Pressed", x, y)
            self.point = (x, y)

    def _set_callback(self):
        if self.passed and not self.setted:
            cv2.setMouseCallback("Frame", self.click)
            self.setted = True
        return self

    def _process(self, frame):
        self._set_callback()
        cv2.circle(frame, self.point, self.radius, self.color, self.line_width)
        self.passed = True
        return frame


def main():
    """ Método de teste. """
    OpenCvVideoCapture(middleware=SimpleCapture(), win_name="Frame").execute()


if __name__ == '__main__':
    main()
