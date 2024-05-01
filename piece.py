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

    if piece == Type.PAWN.value:
        # Normal move
        direction = 1 if color == Color.WHITE.value else -1
        if board.get_piece(row+direction, file) == Type.NONE.value:
            valid_moves.append([row+direction, file])
            valid_moves.append([row+(direction*2), file]) if board.get_piece(row+(direction*2), file) == Type.NONE.value else None

        # Taking a piece
        valid_moves.append([row+direction,file+direction]) if board.get_color(row+direction, file+direction) == Color.BLACK.value else None
        valid_moves.append([row+direction,file-direction]) if board.get_color(row+direction, file-direction) == Color.BLACK.value else None

        # En passant
        valid_moves.append(board.en_passant_target) if (board.en_passant_target[0] == row+1 and (board.en_passant_target[1] == file+1 or board.en_passant_target[1] == file-1) and color == Color.WHITE.value) else None
        valid_moves.append(board.en_passant_target) if (board.en_passant_target[0] == row-1 and (board.en_passant_target[1] == file+1 or board.en_passant_target[1] == file-1) and color == Color.BLACK.value) else None

    return valid_moves
