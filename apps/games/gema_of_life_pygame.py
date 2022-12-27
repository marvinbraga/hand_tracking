# (hand-tracking-py3.10) PS D:\python\computer_vision\hand_tracking>
# inv say "Implemente em python utilizando o pygame o coway game of life."
import random

import pygame

# initialize pygame
pygame.init()

# set up the window
width, height = 500, 500
screen = pygame.display.set_mode((width, height))

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# draw on the surface object
screen.fill(BLACK)

# set up the block size
block_width, block_height = 10, 10

# set up the number of cells
no_rows = int(width / block_width)
no_columns = int(height / block_height)

# set up the cell structure
cells = [[False for x in range(no_columns)] for y in range(no_rows)]

# create a random cell structure
for row in range(no_rows):
    for column in range(no_columns):
        cells[row][column] = random.randint(0, 1)

# Used to manage how fast the screen updates
clock = pygame.time.Clock()


def check(is_running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # create a new random cell structure
            for r in range(no_rows):
                for c in range(no_columns):
                    cells[r][c] = random.randint(0, 1)
    return is_running


def draw():
    for r in range(no_rows):
        for c in range(no_columns):
            color = BLACK
            if cells[r][c]:
                color = GREEN
            pygame.draw.rect(
                screen,
                color,
                [
                    r * block_width,
                    c * block_height,
                    block_width,
                    block_height,
                ],
            )


def apply():
    new_cells = [[False for x in range(no_columns)] for y in range(no_rows)]
    for r in range(no_rows):
        for c in range(no_columns):
            # count the neighbours
            n_neighbours = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    if (
                        r + i >= 0
                        and r + i < no_rows
                        and c + j >= 0
                        and c + j < no_columns
                    ):
                        if cells[r + i][c + j]:
                            n_neighbours += 1
            # apply the rules
            if cells[r][c]:
                new_cells[r][c] = not (n_neighbours < 2 or n_neighbours > 3)
            else:
                new_cells[r][c] = n_neighbours == 3
    return new_cells


# main loop
running = True
while running:
    # check for events
    running = check(running)
    # draw the cell structure
    draw()
    # update the cell structure
    cells = apply()
    # Limit to 60 frames per second
    clock.tick(10)
    # update the display
    pygame.display.flip()

# close the window
pygame.quit()
