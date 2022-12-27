import matplotlib.pyplot as plt
import numpy as np


# função que inicializa o jogo
def init_game(rows, cols):
    state = np.random.randint(2, size=(rows, cols))
    return state


# função que calcula o número de vizinhos vivos
def count_neighbours(state, row, col):
    n_row, n_col = state.shape
    c = 0
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if (
                not (i == 0 and j == 0)
                and 0 <= row + i < n_row
                and 0 <= col + j < n_col
                and state[row + i, col + j]
            ):
                c += 1
    return c


# função que atualiza o estado do jogo
def update_state(state):
    n_row, n_col = state.shape
    next_state = np.zeros((n_row, n_col))
    for row in range(n_row):
        for col in range(n_col):
            n_neighbours = count_neighbours(state, row, col)
            if state[row, col]:
                if n_neighbours == 2 or n_neighbours == 3:
                    # vive
                    next_state[row, col] = 1
            else:
                if n_neighbours == 3:
                    # nascimento
                    next_state[row, col] = 1
    return next_state


# função que renderiza o jogo
def render_game(state):
    plt.imshow(state, interpolation="none", cmap="binary")
    plt.show()


# inicializa o jogo
rows = 50
cols = 50
state = init_game(rows, cols)

# executa o jogo
while True:
    render_game(state)
    state = update_state(state)
