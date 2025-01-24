"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    moves = 0
    moves += sum(row.count(X) + row.count(O) for row in board)
    if moves % 2 == 0:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i, row in enumerate(board):
        for j, state in enumerate(row):
            if state == EMPTY:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    i = action[0]
    j = action[1]

    if new_board[i][j] != EMPTY:
        raise ValueError(f"cannot make move {action} on board")
    new_board[i][j] = player(board)


    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    streaks = {
        'x': 0,
        'o': 0,
    }
    # Check horizontally
    for i, row in enumerate(board):
        if row.count(X) == 3:
            return X
        elif row.count(O) == 3:
            return O

        # Check vertically
        for j in range(3):
            if board[i][j] == X:
                streaks['x'] += 1
            if board[i][j] == O:
                streaks['o'] += 1
        if streaks['o'] == 3:
            return O
        elif streaks['x'] == 3:
            return X
        streaks['o'] = 0
        streaks['x'] = 0

    # Check diagonally
    for i in range


        
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    return
    raise NotImplementedError

test = [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, X],
    ]

def main():
    actions(test)


if __name__ == "__main__":
    main()
    sth = None

"""
[
    [EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY],
]
"""