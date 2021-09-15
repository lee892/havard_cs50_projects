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
    if board == initial_state():
        player = X
    else:
        x_turns = 0
        o_turns = 0
        for i in range(3):
            for j in range(3):
                if board[i][j] == X:
                    x_turns += 1
                elif board[i][j] == O:
                    o_turns += 1
        if x_turns > o_turns:
            player = O
        else:
            player = X

    return player

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_moves.add((i, j))

    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)
    turn = player(board_copy)
    row, column = action
    if board_copy[row][column] is not EMPTY:
        raise NameError("Not a valid action")
    if turn == X:
        board_copy[row][column] = X
    elif turn == O:
        board_copy[row][column] = O

    return board_copy

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    def check_row(board, i, j, turn):
        if board[i][j] == turn and board[i][j + 1] == turn and board[i][j + 2] == turn:
            return True
        return False

    def check_column(board, i, j, turn):
        if board[i][j] == turn and board[i + 1][j] == turn and board[i + 2][j] == turn:
            return True
        return False

    def check_diagonals(board, turn):
        diagonal = True
        anti_diagonal = True
        j = 2
        for i in range(3):
            if board[i][i] != turn:
                diagonal = False
            if board[i][j] != turn:
                anti_diagonal = False
            j -= 1

        if diagonal or anti_diagonal:
            return True
        return False

    if check_diagonals(board, X):
        return X
    elif check_diagonals(board, O):
        return O

    for i in range(3):
        for j in range(3):
            if j < 1:
                if check_row(board, i, j, X):
                    return X
                if check_row(board, i, j, O):
                    return O
            if i < 1:
                if check_column(board, i, j, X):
                    return X
                if check_column(board, i, j, O):
                    return O
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def max_value(board, alpha, beta):
        if terminal(board):
            return utility(board), (0, 0)

        maxv = -2
        for action in actions(board):
            m, _ = min_value(result(board, action), alpha, beta)
            if m > maxv:
                maxv = m
                optimal_action = action
            if maxv >= beta:
                return (maxv, optimal_action)
            if maxv > alpha:
                alpha = maxv

        return (maxv, optimal_action)

    def min_value(board, alpha, beta):
        if terminal(board):
            return utility(board), (0, 0)

        minv = 2
        for action in actions(board):
            m, _ = max_value(result(board, action), alpha, beta)
            if m < minv:
                minv = m
                optimal_action = action
            if minv <= alpha:
                return (minv, optimal_action)
            if minv < beta:
                beta = minv

        return (minv, optimal_action)

    if terminal(board):
        return None

    if player(board) == X:
        value, optimal_action = max_value(board, -2, 2)
    elif player(board) == O:
        value, optimal_action = min_value(board, -2, 2)

    return optimal_action
