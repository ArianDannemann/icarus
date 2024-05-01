from enum import Enum

import board

class Color(Enum):
    """
    Types of chess pieces
    """
    NONE  = 0
    WHITE = 1
    BLACK = 2

class Type(Enum):
    """
    Types of chess pieces
    """
    NONE    = 0
    PAWN    = 1
    KING    = 2
    QUEEN   = 3
    ROOK    = 4
    BISHOP  = 5
    KNIGHT  = 6

def get_valid_moves(row, file):
    """
    Returns all valid positions for piece at row and file
    Returns 2d array of rows and files: [ [row,file], ... ]
    """

    piece = board.get_piece(row, file)
    color = board.get_color(row, file)

    valid_moves = []

    if piece == Type.PAWN:
        # Normal move
        direction = 1 if color == Color.WHITE else -1
        if board.get_piece(row+direction, file) == Type.NONE:
            valid_moves.append([row+direction, file])
            valid_moves.append([row+(direction*2), file]) if board.get_piece(row+(direction*2), file) == Type.NONE else None

        # Taking a piece
        valid_moves.append([row+direction,file+direction]) if board.get_color(row+direction, file+direction) == Color.BLACK else None
        valid_moves.append([row+direction,file-direction]) if board.get_color(row+direction, file-direction) == Color.BLACK else None

        # En passant
        valid_moves.append(board.en_passant_target) if (board.en_passant_target[0] == row+1 and (board.en_passant_target[1] == file+1 or board.en_passant_target[1] == file-1) and color == Color.WHITE) else None
        valid_moves.append(board.en_passant_target) if (board.en_passant_target[0] == row-1 and (board.en_passant_target[1] == file+1 or board.en_passant_target[1] == file-1) and color == Color.BLACK) else None

    # Remove moves that are now withing the bounds of the board
    i = 0
    for valid_move in valid_moves:
        i+=1
        if valid_move[0] > 7 or valid_move[0] < 0 or valid_move[1] > 7 or valid_move[1] < 0:
            valid_moves.pop(i)
            i-=1

    return valid_moves
