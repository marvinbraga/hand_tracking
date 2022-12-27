import random

import pygame


class Setup:
    # set up the colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    GRAY = (99, 99, 99)

    def __init__(
        self,
        width=100,
        height=100,
        cell_size=3,
        cell_color=GREEN,
        background_color=GRAY,
    ):
        """
        Init grid size and cell size.
        """
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cell_color = cell_color
        self.background_color = background_color


class Cell:
    """
    Represent a cell in the grid.
    """

    def __init__(self, x, y, setup):
        self.setup = setup
        self.x = x
        self.y = y
        self.alive = random.randint(0, 1)

    def draw(self, surface):
        if self.alive:
            pos = (
                self.x * self.setup.cell_size,
                self.y * self.setup.cell_size,
                self.setup.cell_size,
                self.setup.cell_size,
            )
            pygame.draw.rect(surface, self.setup.cell_color, pos)

    def __repr__(self):
        return f"<Cell: {self.x}, {self.y}, alive={self.alive}>"


class Grid:
    """
    Represent the grid of cells.
    """

    def __init__(self, setup):
        self.setup = setup
        self.width = setup.width
        self.height = setup.height
        self.grid = [
            [Cell(x, y, self.setup) for x in range(setup.width)]
            for y in range(setup.height)
        ]
        self.clock = pygame.time.Clock()

        # Create a Pygame window with the desired size
        self.screen = pygame.display.set_mode(
            (
                self.setup.width * self.setup.cell_size,
                self.setup.height * self.setup.cell_size,
            ),
        )

    def count_live_neighbors(self, x, y):
        """
        Count the number of live neighbors for a given cell.
        """
        neighbors = [
            self.grid[i][j]
            for i in range(x - 1, x + 2)
            for j in range(y - 1, y + 2)
            if (0 <= i < self.width)
            and (0 <= j < self.height)
            and not (i == x and j == y)
        ]
        return sum(cell.alive for cell in neighbors)

    def update(self):
        """
        Update the state of each cell in the grid
        """
        # Clear the screen
        self.screen.fill(self.setup.background_color)
        for cell in self:
            # Count the number of live neighbors for this cell
            live_neighbors = self.count_live_neighbors(cell.x, cell.y)

            # Apply the rules of the Game of Life to update the cell's state
            cell.alive = (
                (live_neighbors == 3) if not cell.alive else (2 <= live_neighbors <= 3)
            )
        return self

    def draw(self, surface):
        """
        Draw the cells onto the screen.
        """
        for cell in self:
            cell.draw(surface)
        # Limit to 60 frames per second
        self.clock.tick(10)
        pygame.display.flip()
        return self

    def __iter__(self):
        """
        Define an iterator for the grid to allow it to be iterated over like a list
        """
        self.iter_index = 0
        return self

    def __next__(self):
        if self.iter_index >= self.width * self.height:
            raise StopIteration
        else:
            x = self.iter_index % self.width
            y = self.iter_index // self.width
            self.iter_index += 1
            return self.grid[x][y]


if __name__ == "__main__":

    def check(is_running, grid_instance):
        # check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # create a new random cell structure
                grid_instance = None
        return is_running, grid_instance

    grid = None
    pygame.init()

    # Setup to apply
    config = Setup(cell_size=10)

    running = True
    while running:
        running, grid = check(running, grid)

        if not grid:
            grid = Grid(config)

        grid.update().draw(grid.screen)

    # close the window
    pygame.quit()
