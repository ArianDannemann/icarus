"""
Handles piece positioning and moving on a board
"""

import piece
import position

board = [ 0 ] * 64
color = [ 0 ] * 64

en_passant_target = [ -1, -1 ]
en_passant_victim = [ -1, -1 ]
en_passant_valid = False

promotion_target = piece.Type.NONE

def setup():
    """
    Sets up the default chess position
    """

    set_piece(0, 0, piece.Type.ROOK, piece.Color.WHITE)
    set_piece(0, 1, piece.Type.KNIGHT, piece.Color.WHITE)
    set_piece(0, 2, piece.Type.BISHOP, piece.Color.WHITE)
    set_piece(0, 3, piece.Type.QUEEN, piece.Color.WHITE)
    set_piece(0, 4, piece.Type.KING, piece.Color.WHITE)
    set_piece(0, 5, piece.Type.BISHOP, piece.Color.WHITE)
    set_piece(0, 6, piece.Type.KNIGHT, piece.Color.WHITE)
    set_piece(0, 7, piece.Type.ROOK, piece.Color.WHITE)
    set_piece(1, 0, piece.Type.PAWN, piece.Color.WHITE)
    set_piece(1, 1, piece.Type.PAWN, piece.Color.WHITE)
    set_piece(1, 2, piece.Type.PAWN, piece.Color.WHITE)
    set_piece(1, 3, piece.Type.PAWN, piece.Color.WHITE)
    set_piece(1, 4, piece.Type.PAWN, piece.Color.WHITE)
    set_piece(1, 5, piece.Type.PAWN, piece.Color.WHITE)
    set_piece(1, 6, piece.Type.PAWN, piece.Color.WHITE)
    set_piece(1, 7, piece.Type.PAWN, piece.Color.WHITE)

    set_piece(7, 0, piece.Type.ROOK, piece.Color.BLACK)
    set_piece(7, 1, piece.Type.KNIGHT, piece.Color.BLACK)
    set_piece(7, 2, piece.Type.BISHOP, piece.Color.BLACK)
    set_piece(7, 3, piece.Type.QUEEN, piece.Color.BLACK)
    set_piece(7, 4, piece.Type.KING, piece.Color.BLACK)
    set_piece(7, 5, piece.Type.BISHOP, piece.Color.BLACK)
    set_piece(7, 6, piece.Type.KNIGHT, piece.Color.BLACK)
    set_piece(7, 7, piece.Type.ROOK, piece.Color.BLACK)
    set_piece(6, 0, piece.Type.PAWN, piece.Color.BLACK)
    set_piece(6, 1, piece.Type.PAWN, piece.Color.BLACK)
    set_piece(6, 2, piece.Type.PAWN, piece.Color.BLACK)
    set_piece(6, 3, piece.Type.PAWN, piece.Color.BLACK)
    set_piece(6, 4, piece.Type.PAWN, piece.Color.BLACK)
    set_piece(6, 5, piece.Type.PAWN, piece.Color.BLACK)
    set_piece(6, 6, piece.Type.PAWN, piece.Color.BLACK)
    set_piece(6, 7, piece.Type.PAWN, piece.Color.BLACK)

def display():
    """
    Print the current board layout to console
    """

    print("")
    for row in range(7, -1, -1):
        print(f" {row}:  ", end="")
        for file in range(0, 8):
            piece_type = get_piece(row, file)
            piece_color = get_color(row, file)

            if piece_type == piece.Type.PAWN:
                print("P" if piece_color == piece.Color.WHITE else "p", end=" ")
            if piece_type == piece.Type.KING:
                print("K" if piece_color == piece.Color.WHITE else "k", end=" ")
            if piece_type == piece.Type.QUEEN:
                print("Q" if piece_color == piece.Color.WHITE else "q", end=" ")
            if piece_type == piece.Type.ROOK:
                print("R" if piece_color == piece.Color.WHITE else "r", end=" ")
            if piece_type == piece.Type.KNIGHT:
                print("N" if piece_color == piece.Color.WHITE else "n", end=" ")
            if piece_type == piece.Type.BISHOP:
                print("B" if piece_color == piece.Color.WHITE else "b", end=" ")
            if piece_type == piece.Type.NONE:
                print("  ", end="")

        print("")
    print("\n     0 1 2 3 4 5 6 7")

def get_piece(row, file, b=board):
    """
    Returns the piece at row and file
    """

    if row > 7 or row < 0 or file > 7 or file < 0:
        return piece.Type.NONE

    return piece.Type(b[(row*8) + file])

def set_piece(row, file, type=piece.Type.PAWN, color=piece.Color.WHITE, b=board, c=color):
    """
    Sets piece at row and file to type
    """

    if row > 7 or row < 0 or file > 7 or file < 0:
        return

    b[(row*8) + file] = type.value
    set_color(row, file, color, c)

def get_color(row, file, c=color):
    """
    Gets color of piece at row and file
    """

    if row > 7 or row < 0 or file > 7 or file < 0:
        return piece.Color.NONE

    return piece.Color(c[(row*8) + file])

def set_color(row, file, new_color, c=color):
    """
    Sets color of piece at row and file to color
    """

    if row > 7 or row < 0 or file > 7 or file < 0:
        return

    c[(row*8) + file] = new_color.value

def teleport_piece(row, file, new_row, new_file, b=board, c=color):
    """
    Teleports piece from row and file to new_row and new_file
    while ignoring all chess rules
    """

    set_piece(new_row, new_file, piece.Type(get_piece(row, file, b)), piece.Color(get_color(row, file, c)), b, c)
    set_piece(row, file, piece.Type.NONE, piece.Color.NONE, b, c)

def move_piece(row, file, new_row, new_file, b=board, c=color):
    """
    Moves piece from row and file to new_row and new_file
    according to chess rules
    Returns 1 if move was legal, 0 otherwise
    """

    global en_passant_target
    global en_passant_victim
    global en_passant_valid
    global promotion_target

    result = 0
    found_en_passant = False

    for valid_move in piece.get_valid_moves(row, file):
        if position.equals(valid_move, [new_row, new_file]):

            teleport_piece(row, file, new_row, new_file, b, c)

            # Check if en passant was done
            if (get_piece(new_row, new_file, b) == piece.Type.PAWN
            and position.equals(en_passant_target, [new_row, new_file])
            and en_passant_valid):
                set_piece(en_passant_victim[0], en_passant_victim[1], piece.Type.NONE, piece.Color.NONE, b, c)

            # Check if en passant can be done in the next move
            if get_piece(new_row, new_file, b) == piece.Type.PAWN and abs(row-new_row) > 1:
                en_passant_target = (
                    [new_row-1, new_file]
                    if get_color(new_row, new_file, c) == piece.Color.WHITE else
                    [new_row+1, new_file]
                )
                en_passant_victim = ([new_row, new_file])
                found_en_passant = True

            # Check for promotion
            if get_piece(new_row, new_file, b) == piece.Type.PAWN and (new_row == 7 or new_row == 0):
                set_piece(new_row, new_file, promotion_target, piece.Color(get_color(new_row, new_file, b)), b, c)

            result = 1
            break

    en_passant_valid = (result == 1 and found_en_passant)
    if not en_passant_valid:
        en_passant_target = [-1,-1]

    return result

def copy(b=board, c=color):
    """
    Returns a copy of board and color arrays
    """

    return b.copy(), c.copy()
