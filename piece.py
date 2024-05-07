"""
Handles rules for pieces
"""

from enum import Enum

import board
import position

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

def get_valid_moves(row, file, simulate=True, b=None, c=None):
    """
    Returns all valid positions for piece at row and file
    Returns 2d array of rows and files: [ [row,file], ... ]
    """

    b = b if b is not None else board.board
    c = c if c is not None else board.color

    piece = board.get_piece(row, file, b)
    color = board.get_color(row, file, c)

    valid_moves = []

    if piece == Type.PAWN:
        valid_moves = get_pawn_moves(row, file, color, c)

    if piece == Type.BISHOP:
        valid_moves.extend(get_line_move(row, file, 1, 1, color, c))
        valid_moves.extend(get_line_move(row, file, 1, -1, color, c))
        valid_moves.extend(get_line_move(row, file, -1, -1, color, c))
        valid_moves.extend(get_line_move(row, file, -1, 1, color, c))

    if piece == Type.ROOK:
        valid_moves.extend(get_line_move(row, file, 0, 1, color, c))
        valid_moves.extend(get_line_move(row, file, 0, -1, color, c))
        valid_moves.extend(get_line_move(row, file, 1, 0, color, c))
        valid_moves.extend(get_line_move(row, file, -1, 0, color, c))

    if piece == Type.QUEEN:
        valid_moves.extend(get_line_move(row, file, 1, 1, color, c))
        valid_moves.extend(get_line_move(row, file, 1, -1, color, c))
        valid_moves.extend(get_line_move(row, file, -1, -1, color, c))
        valid_moves.extend(get_line_move(row, file, -1, 1, color, c))
        valid_moves.extend(get_line_move(row, file, 0, 1, color, c))
        valid_moves.extend(get_line_move(row, file, 0, -1, color, c))
        valid_moves.extend(get_line_move(row, file, 1, 0, color, c))
        valid_moves.extend(get_line_move(row, file, -1, 0, color, c))

    if piece == Type.KING:
        valid_moves.extend(get_king_moves(row, file, color, c))

    if piece == Type.KNIGHT:
        valid_moves.extend(get_knight_moves(row, file, color, c))

    # Check if the move would place the king in check
    if simulate:
        i = 0
        while i < len(valid_moves):
            valid_move = valid_moves[i]
            copied_board, copied_color = board.copy()
            color = board.get_color(row, file, copied_color)
            other_color = Color.WHITE if color == Color.BLACK else Color.BLACK

            board.teleport_piece(row, file, valid_move[0], valid_move[1], copied_board, copied_color)

            _, result = get_all_moves(other_color, copied_board, copied_color)

            if result:
                valid_moves.pop(i)
                i-=1

            i+=1

    return valid_moves

def get_knight_moves(row, file, color=None, c=None):
    """
    Returns all valid positions for a knight at row and file
    Returns 2d array of rows and files: [ [row,file], ... ]
    """

    c = c if c is not None else board.color
    color = board.get_color(row, file, c) if color is None else color

    valid_moves = [
        [row+2,file+1],
        [row+2,file-1],
        [row-2,file+1],
        [row-2,file-1],
        [row+1,file+2],
        [row-1,file+2],
        [row+1,file-2],
        [row-1,file-2],
    ]

    # Remove moves that are now withing the bounds of the board
    i = 0
    while i < len(valid_moves):
        if valid_moves[i][0] > 7 or valid_moves[i][0] < 0 or valid_moves[i][1] > 7 or valid_moves[i][1] < 0 or board.get_color(valid_moves[i][0], valid_moves[i][1], c) == color:
            valid_moves.pop(i)
            i-=1

        i+=1

    return valid_moves

def get_king_moves(row, file, color=None, c=None):
    """
    Returns all valid positions for a king at row and file
    Returns 2d array of rows and files: [ [row,file], ... ]
    """
    # TODO - castle

    c = c if c is not None else board.color
    color = board.get_color(row, file, c) if color is None else color

    valid_moves = []

    for off_x in range(-1, 2):
        for off_y in range(-1, 2):

            if off_x == 0 and off_y == 0:
                continue

            current_row = row + off_x
            current_file = file + off_y

            if not position.is_in_bounds([current_row, current_file]):
                continue

            if board.get_color(current_row, current_file, c) != color:
                valid_moves.append([current_row, current_file])

    castle_info = board.white_castle_info if color == Color.WHITE else board.black_castle_info
    if not castle_info[0]:
        if not castle_info[1]:
            valid_moves.append([row,file-2])
        if not castle_info[2]:
            valid_moves.append([row,file+2])

    return valid_moves

def get_pawn_moves(row, file, color=None, c=None):
    """
    Returns all valid positions for a pawn at row and file
    Returns 2d array of rows and files: [ [row,file], ... ]
    """

    c = c if c is not None else board.color
    color = color if color is not None else board.get_color(row, file, c)

    valid_moves = []

    direction = 1 if color == Color.WHITE else -1
    step_one        = [ row+direction, file ]
    step_two        = [ row+(direction*2), file ]
    attack_left     = [ row+direction, file+1 ]
    attack_right    = [ row+direction, file-1]

    # Normal move
    if board.get_color(step_one[0], step_one[1], c) == Color.NONE:
        valid_moves.append(step_one)

        # First row move
        if (board.get_color(step_two[0], step_two[1], c) == Color.NONE
        and (row==1 if color == Color.WHITE else row==6)):
            valid_moves.append(step_two)

    # Taking a piece
    if board.get_color(attack_left[0], attack_left[1], c) not in (color, Color.NONE):
        valid_moves.append(attack_left)
    if board.get_color(attack_right[0], attack_right[1], c) not in (color, Color.NONE):
        valid_moves.append(attack_right)

    # En passant
    if position.equals(board.en_passant_target, attack_left):
        valid_moves.append(board.en_passant_target)
    if position.equals(board.en_passant_target, attack_right):
        valid_moves.append(board.en_passant_target)

    # Remove moves that are now withing the bounds of the board
    i = 0
    while i < len(valid_moves):
        if (not position.is_in_bounds(valid_moves[i])
        or board.get_color(valid_moves[i][0], valid_moves[i][1]) == color):
            valid_moves.pop(i)
            i-=1
        i+=1

    return valid_moves

def get_line_move(row, file, dir_row, dir_file, color=None, c=None):
    """
    Returns all valid positions for piece at row and file in the direction of dir_row and dir_file
    For everystep in the line search we change row+=dir_row and file+=dir_file
    Returns 2d array of rows and files: [ [row,file], ... ]
    """

    c = c if c is not None else board.color
    color = board.get_color(row, file, c) if color is None else color

    valid_moves = []

    for i in range(1, 8):
        current_row = row + (dir_row*i)
        current_file = file + (dir_file*i)

        if current_row > 7 or current_row < 0 or current_file > 7 or current_file < 0:
            break

        current_color = board.get_color(current_row, current_file, c)

        if current_color != color:
            valid_moves.append([current_row, current_file])

        if current_color != Color.NONE:
            break

    return valid_moves

# NOTE - active_board and active_color should be board.board and board.color
#        the None attribute was set to prevent circular imports
def get_all_moves(color, b=None, c=None):
    """
    Returns all valid moves for all pieces of a certain color
    Returns 2d array of rows and files: [ [row,file], ... ]
    Also returns true if the enemy king is in check, false if otherwise
    """

    b = b if b is not None else board.board
    c = c if c is not None else board.color

    valid_moves = []
    enemy_in_check = False

    for row in range(0, 8):
        for file in range(0, 8):

            if board.get_color(row, file, c) != color:
                continue

            piece_moves = get_valid_moves(row, file, False, b, c)
            valid_moves.extend(piece_moves)

            # Check if we are checking the king
            for piece_move in piece_moves:
                if board.get_color(piece_move[0], piece_move[1], c) != color and board.get_piece(piece_move[0], piece_move[1], b) == Type.KING:
                    enemy_in_check = True

    return valid_moves, enemy_in_check
