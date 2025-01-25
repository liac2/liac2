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

    if new_board[i][j] != EMPTY or i < 0 or i > 2 or j < 0 or j > 2:
        raise ValueError(f"cannot make move {action} on board")
    new_board[i][j] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    for j in range(3):
        streaks = []

        for i, row in enumerate(board):
        
            # Check horizontally
            if j < 1:
                if row.count(X) == 3:
                    return X
                elif row.count(O) == 3:
                    return O

            # Check vertically
            streaks.append(board[i][j])
        
        if streaks.count(X) == 3 or streaks.count(O) == 3:
            return streaks[0]

    # Check diagonally
    d_streak = []
    streaks = []
    for i, row in enumerate(board):
        d_streak.append(row[i])
        reverse_i = -1 - i
        streaks.append(row[reverse_i])
    if streaks.count(X) == 3 or streaks.count(O) == 3:
        return streaks[0]
    elif d_streak.count(X) == 3 or d_streak.count(O) == 3:
        return d_streak[0]
        
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board=board):
        return True
    elif sum(row.count(EMPTY) for row in board) == 0:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board=board) 
    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None
    
    turn = player(board)
    moves = actions(board)

    best_move = list(moves)[0]
    if turn == X:
        v = float('-inf')

        # Get value for every move
        for move in moves:
            new_state = result(board, move)
            value = min_value(new_state, v)
            if v < value:
                v = value
                best_move = move

    else:
        v = float('inf')

        # Get value for every move
        for move in moves:
            new_state = result(board, move)
            value = max_value(new_state, v)
            if v > value:
                v = value
                best_move = move

    return best_move
    

def max_value(board, max_value):
    if terminal(board):
        return utility(board)
    
    moves = actions(board)

    v = float('-inf')

    # Get value for every move
    for move in moves:
        move = result(board, move)
        v = max(v, min_value(move, v))
        if v > max_value:
            break
    return v


def min_value(board, min_value):
    if terminal(board):
        return utility(board)

    moves = actions(board)

    v = float('inf')

    # Get value for every move
    for move in moves:
        move = result(board, move)
        v = min(v, max_value(move, v))
        if v < min_value:
            break

    return v
    

test = [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
    ]

def main():
    winner(test)


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