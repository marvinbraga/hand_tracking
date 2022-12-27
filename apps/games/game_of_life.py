import time

import numpy as np


# Cria uma matriz de NxN
def init_grid(N):
    grid = np.zeros((N, N))
    return grid


# Popula a matriz
def populate(grid, prob):
    N = grid.shape[0]

    for i in range(N):
        for j in range(N):
            if np.random.random() < prob:
                grid[i, j] = 1
    return grid


# Atualiza a matriz de acordo com as regras do jogo
def update(grid):
    N = grid.shape[0]
    new_grid = np.zeros((N, N))

    for i in range(N):
        for j in range(N):
            total = int(
                grid[i, (j - 1) % N]
                + grid[i, (j + 1) % N]
                + grid[(i - 1) % N, j]
                + grid[(i + 1) % N, j]
                + grid[(i - 1) % N, (j - 1) % N]
                + grid[(i - 1) % N, (j + 1) % N]
                + grid[(i + 1) % N, (j - 1) % N]
                + grid[(i + 1) % N, (j + 1) % N],
            )

            # Regra 1
            if grid[i, j] == 1 and (total < 2 or total > 3):
                new_grid[i, j] = 0

            # Regra 2
            elif grid[i, j] == 0 and total == 3:
                new_grid[i, j] = 1

            # Regra 3
            else:
                new_grid[i, j] = grid[i, j]

    return new_grid


# Exibe a matriz atualizada
def display(grid):
    N = grid.shape[0]

    for i in range(N):
        for j in range(N):
            if grid[i, j] == 0:
                print(".", end="")
            else:
                print("#", end="")
        print()


# Roda o jogo
def main():
    N = 20
    grid = init_grid(N)
    grid = populate(grid, 0.2)
    print("Geração 0")
    display(grid)

    for i in range(1, 10):
        time.sleep(1)
        grid = update(grid)
        print(f"Geração {i}")
        display(grid)


if __name__ == "__main__":
    main()
