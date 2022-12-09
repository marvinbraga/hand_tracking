import cv2

from core.abstract_middleware import BaseMiddleware
from core.video_capture import OpenCvCanvas


class SimpleCapture(BaseMiddleware):
    passed, setted, pressed = False, False, False
    radius = 3
    color = (0, 255, 0)
    _canvas = None

    def _paint(self, x, y):
        cv2.circle(self._canvas, (x, y), self.radius, self.color, -1)

    def _click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.pressed = True
            self._paint(x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            self.pressed = False
        if self.pressed and event == cv2.EVENT_MOUSEMOVE:
            self._paint(x, y)

    def _set_callback(self):
        if not self.setted and self.passed:
            cv2.setMouseCallback("Canvas", self._click)
            self.setted = True
        return self

    def _update_color(self):
        if cv2.waitKey(1) & 0xFF == ord('b'):
            self.color = (255, 0, 0)
        elif cv2.waitKey(1) & 0xFF == ord('g'):
            self.color = (0, 255, 0)
        elif cv2.waitKey(1) & 0xFF == ord('r'):
            self.color = (0, 0, 255)
        return self

    def _process(self, frame):
        self._canvas = frame
        self._set_callback()._update_color().passed = True
        return self._canvas


def main():
    """ Método de teste. """
    OpenCvCanvas(middleware=SimpleCapture(), win_name="Canvas").execute()


if __name__ == '__main__':
    main()
