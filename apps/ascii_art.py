import pygame as pg
import numpy as np
import cv2


class ArtConverter:

    ASCII_CHARS = '.",:;!~+-XMO*w&8@'
    ASCII_COEFF = 255 // (len(ASCII_CHARS) - 1)

    def __init__(self, path, font_size=12):
        pg.init()
        self.cap = cv2.VideoCapture(0)

        self.font_size = font_size
        self.path = path
        self.cv2_image = None
        self.image = None
        self.load_image()
        self.res = self.width, self.height = self.image.shape[0], self.image.shape[1]
        self.surface = pg.display.set_mode(self.res)
        self.clock = pg.time.Clock()

        self.font = pg.font.SysFont('Courier', self.font_size, bold=True)
        self.char_step = int(self.font_size * 0.6)
        self.rendered_ascii_chars = self.set_rendered_chars()

    def load_image(self):
        ret, self.cv2_image = self.cap.read()  # cv2.imread(self.path)
        self.image = self.get_image()

    def set_rendered_chars(self):
        return [self.font.render(char, False, 'white') for char in self.ASCII_CHARS]

    def get_image(self):
        transposed_image = cv2.transpose(self.cv2_image)
        # rgb_image = cv2.cvtColor(transposed_image, cv2.COLOR_RGB2BGR)
        bw_image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2GRAY)
        return bw_image

    def draw_cv2_image(self):
        resized_cv2_image = cv2.resize(
            self.cv2_image, (640, int(self.height * 640 / self.width)), interpolation=cv2.INTER_AREA)
        cv2.imshow('img', resized_cv2_image)

    def draw_converted_image(self):
        char_indices = self.image // self.ASCII_COEFF
        for x in range(0, self.width, self.char_step):
            for y in range(0, self.height, self.char_step):
                char_index = char_indices[x, y]
                if char_index:
                    try:
                        self.surface.blit(self.rendered_ascii_chars[char_index], (x, y))
                    except Exception:
                        pass

    def save_image(self):
        pygame_image = pg.surfarray.array3d(self.surface)
        cv2_img = cv2.transpose(pygame_image)
        cv2.imwrite('data\\ascii_converted_image.jpg', cv2_img)

    def draw(self):
        self.surface.fill('black')
        self.draw_converted_image()
        self.draw_cv2_image()

    def run(self):
        while True:
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()
                elif i.type == pg.KEYDOWN:
                    if i.key == pg.K_s:
                        self.save_image()
            self.load_image()
            self.draw()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick()


class ArtConverterColor(ArtConverter):
    
    ASCII_CHARS_CLEAR = list("Ñ@#W$9876543210?:abc;:+=-,._ ")
    ASCII_CHARS = ASCII_CHARS_CLEAR[::-1]
    # ASCII_CHARS = ' ixzao*#MW&8%B@$'

    def __init__(self, color_lvl=8, *args, **kwargs):
        self.gray_image = None
        super().__init__(**kwargs)
        self.color_lvl = color_lvl
        self.palette, self.color_coeff = self.create_palette()

    def load_image(self):
        self.image, self.gray_image = self.get_image()

    def get_image(self):
        ret, self.cv2_image = self.cap.read()  # cv2.imread(self.path)
        transposed_image = cv2.transpose(self.cv2_image)
        image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2RGB)
        bw_image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2GRAY)
        return image, bw_image

    def create_palette(self):
        colors, color_coeff = np.linspace(0, 255, num=self.color_lvl, dtype=int, retstep=True)
        color_palette = [np.array([r, g, b]) for r in colors for g in colors for b in colors]
        palette = dict.fromkeys(self.ASCII_CHARS, None)
        color_coeff = int(color_coeff)
        for char in palette:
            char_palette = {}
            for color in color_palette:
                color_key = tuple(color // color_coeff)
                char_palette[color_key] = self.font.render(char, False, tuple(color))
            palette[char] = char_palette
        return palette, color_coeff

    def draw_converted_image(self):
        char_indices = self.gray_image // self.ASCII_COEFF
        color_indices = self.image // self.color_coeff
        for x in range(0, self.width, self.char_step):
            for y in range(0, self.height, self.char_step):
                char_index = char_indices[x, y]
                if char_index:
                    try:
                        char, color = self.ASCII_CHARS[char_index], tuple(color_indices[x, y])
                        self.surface.blit(self.palette[char][color], (x, y))
                    except Exception:
                        pass


if __name__ == '__main__':
    app = ArtConverterColor(path='data\\car_original.jpg')
    app.run()
