import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class TextCv2:
    def __init__(self, frame, font_name, size=8):
        self.size = size
        self.font_name = font_name
        self.image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        self.img_draw = ImageDraw.Draw(self.image)

    def draw(self, pos, text):
        self.img_draw.text(
            pos,
            text,
            font=ImageFont.truetype(self.font_name, self.size),
        )
        return self

    @property
    def text(self):
        return cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)


class AsciiVideo:
    ASCII_CHARS = list("Ñ@#W$9876543210?:abc;:+=-,._ ")
    ASCII_CHARS_DARK = ASCII_CHARS[::-1]

    def __init__(self, new_width=100, is_dark=True):
        self.is_dark = is_dark
        self.new_width = new_width
        self.new_height = 0
        self.image = None
        self.ascii_chars = ""
        self.ascii_image = ""
        self.space = 5
        self.font_index = 0

    def set_image(self, image):
        self.image = image
        return self

    def resize_image(self):
        w, h = self.image.size
        ratio = h / w
        self.new_height = int(self.new_width * ratio)
        self.image = self.image.resize((self.new_width, self.new_height))
        return self

    def clear(self):
        self.ascii_chars = ""
        self.image = None

    def grayify(self):
        self.image = self.image.convert("L")
        return self

    def pixel_to_ascii(self):
        ascii_chars = self.ASCII_CHARS_DARK if self.is_dark else self.ASCII_CHARS
        self.ascii_chars = "".join(
            [ascii_chars[pxl // 25] for pxl in self.image.getdata()],
        )
        return self

    def prepare(self):
        total_pixels = len(self.ascii_chars)
        self.ascii_image = "\n".join(
            [
                self.ascii_chars[index : (index + self.new_width)]
                for index in range(0, total_pixels, self.new_width)
            ],
        )
        self.clear()
        return self

    def text_to_cv(self, image):
        img = image
        for index, line in enumerate(self.ascii_image.split("\n")):
            img = (
                TextCv2(img, "c:\\windows\\fonts\\consola.ttf", 8)
                .draw((0, index * self.space), line)
                .text
            )
        return img


def main(use_cv=False):
    cap = cv2.VideoCapture(0)
    try:
        width = 160
        ascii_video = AsciiVideo(new_width=width)
        while True:
            ret, frame = cap.read()
            cv2.imshow("frame", frame)
            ascii_video.set_image(
                Image.fromarray(frame),
            ).resize_image().grayify().pixel_to_ascii().prepare()

            if use_cv:
                size = Image.fromarray(frame).size[::-1]
                background = np.zeros((*size, 3), dtype=np.uint8)
                cv2.imshow("chars", ascii_video.text_to_cv(background))
            else:
                sys.stdout.write(ascii_video.ascii_image)
                os.system("cls" if os.name == "nt" else "clear")

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main(use_cv=True)
