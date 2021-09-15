import tictactoe as ttt

X = "X"
O = "O"
EMPTY = None

board = [[EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]]

print(dict())
print(ttt.player(board))
print(ttt.minimax(board))