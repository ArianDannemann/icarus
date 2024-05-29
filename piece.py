"""
Holds the classes Color and Type
"""

from enum import Enum
import typing

import board as b
import position


class Color(Enum):
    """
    Types of chess pieces
    """

    NONE = 0
    WHITE = 1
    BLACK = 2


class Type(Enum):
    """
    Types of chess pieces
    """

    NONE = 0
    PAWN = 1
    KING = 2
    QUEEN = 3
    ROOK = 4
    BISHOP = 5
    KNIGHT = 6


def get_valid_moves(row: int, file: int, simulate: bool, board: typing.Any) -> list[list[int]]:
    """
    Returns all valid positions for piece at row and file
    Returns 2d array of rows and files: [ [row,file], ... ]

    board has to be of type board.Board
    """

    piece = board.get_piece(row, file)
    color = board.get_color(row, file)

    valid_moves = []

    if piece == Type.PAWN:
        valid_moves = get_pawn_moves(row, file, board)

    if piece == Type.BISHOP:
        valid_moves.extend(get_line_move(row, file, [1, 1], board))
        valid_moves.extend(get_line_move(row, file, [1, -1], board))
        valid_moves.extend(get_line_move(row, file, [-1, -1], board))
        valid_moves.extend(get_line_move(row, file, [-1, 1], board))

    if piece == Type.ROOK:
        valid_moves.extend(get_line_move(row, file, [0, 1], board))
        valid_moves.extend(get_line_move(row, file, [0, -1], board))
        valid_moves.extend(get_line_move(row, file, [1, 0], board))
        valid_moves.extend(get_line_move(row, file, [-1, 0], board))

    if piece == Type.QUEEN:
        valid_moves.extend(get_line_move(row, file, [1, 1], board))
        valid_moves.extend(get_line_move(row, file, [1, -1], board))
        valid_moves.extend(get_line_move(row, file, [-1, -1], board))
        valid_moves.extend(get_line_move(row, file, [-1, 1], board))
        valid_moves.extend(get_line_move(row, file, [0, 1], board))
        valid_moves.extend(get_line_move(row, file, [0, -1], board))
        valid_moves.extend(get_line_move(row, file, [1, 0], board))
        valid_moves.extend(get_line_move(row, file, [-1, 0], board))

    if piece == Type.KING:
        valid_moves.extend(get_king_moves(row, file, board, simulate))

    if piece == Type.KNIGHT:
        valid_moves.extend(get_knight_moves(row, file, board))

    # Check if the move would place the king in check
    if simulate:
        i = 0
        while i < len(valid_moves):
            valid_move = valid_moves[i]
            copied_board = b.Board()
            copied_board.board, copied_board.color = board.copy()
            color = copied_board.get_color(row, file)
            other_color = Color.WHITE if color == Color.BLACK else Color.BLACK

            copied_board.teleport_piece(
                row,
                file,
                valid_move[0],
                valid_move[1]
            )

            _, result = get_all_moves(other_color, copied_board, False)

            if result:
                valid_moves.pop(i)
                i -= 1

            i += 1

    return valid_moves


def get_knight_moves(row: int, file: int, board: typing.Any) -> list[list[int]]:
    """
    Returns all valid positions for a knight at row and file
    Returns 2d array of rows and files: [ [row,file], ... ]

    board has to be of type board.Board
    """

    color = board.get_color(row, file)

    valid_moves = [
        [row + 2, file + 1],
        [row + 2, file - 1],
        [row - 2, file + 1],
        [row - 2, file - 1],
        [row + 1, file + 2],
        [row - 1, file + 2],
        [row + 1, file - 2],
        [row - 1, file - 2],
    ]

    # Remove moves that are now withing the bounds of the board
    i = 0
    while i < len(valid_moves):
        if (not position.is_in_bounds(valid_moves[i])
                or board.get_color(valid_moves[i][0], valid_moves[i][1]) == color):
            valid_moves.pop(i)
            i -= 1

        i += 1

    return valid_moves


def get_king_moves(row: int,
                   file: int,
                   board: typing.Any,
                   can_castle: bool = True) -> list[list[int]]:
    """
    Returns all valid positions for a king at row and file
    Returns 2d array of rows and files: [ [row,file], ... ]

    board has to be of type board.Board
    """

    valid_moves = []
    color = board.get_color(row, file)
    enemy_color = Color.WHITE if color == Color.BLACK else Color.BLACK
    castle_info = board.white_castle_info if color == Color.WHITE else board.black_castle_info

    for off_x in range(-1, 2):
        for off_y in range(-1, 2):

            if off_x == 0 and off_y == 0:
                continue

            current_row = row + off_x
            current_file = file + off_y

            if not position.is_in_bounds([current_row, current_file]):
                continue

            if board.get_color(current_row, current_file) != color:
                valid_moves.append([current_row, current_file])

    # NOTE - it does not matter here that we use board instead of b
    #        since we dont castle in simulation (we cant take the king through castles)
    # Check for castling
    if not castle_info[0] and can_castle:
        enemy_moves, in_check = get_all_moves(enemy_color, board, False)

        if in_check:
            return valid_moves

        if (not castle_info[1]
                and [row, file - 1] not in enemy_moves
                and [row, file - 2] not in enemy_moves
                and board.get_piece(row, file - 1) == Type.NONE
                and board.get_piece(row, file - 2) == Type.NONE):
            valid_moves.append([row, file - 2])

        if (not castle_info[2]
                and [row, file + 1] not in enemy_moves
                and [row, file + 2] not in enemy_moves
                and board.get_piece(row, file + 1) == Type.NONE
                and board.get_piece(row, file + 2) == Type.NONE):
            valid_moves.append([row, file + 2])

    return valid_moves


def get_pawn_moves(row: int, file: int, board: typing.Any) -> list[list[int]]:
    """
    Returns all valid positions for a pawn at row and file
    Returns 2d array of rows and files: [ [row,file], ... ]

    board has to be of type board.Board
    """

    valid_moves = []
    color = board.get_color(row, file)

    direction = 1 if color == Color.WHITE else -1
    step_one = [row + direction, file]
    step_two = [row + (direction * 2), file]
    attack_left = [row + direction, file + 1]
    attack_right = [row + direction, file - 1]

    # Normal move
    if board.get_color(step_one[0], step_one[1]) == Color.NONE:
        valid_moves.append(step_one)

        # First row move
        if (board.get_color(step_two[0], step_two[1]) == Color.NONE
                and (row == 1 if color == Color.WHITE else row == 6)):
            valid_moves.append(step_two)

    # Taking a piece
    if board.get_color(attack_left[0], attack_left[1]) not in (color, Color.NONE):
        valid_moves.append(attack_left)
    if board.get_color(attack_right[0], attack_right[1]) not in (color, Color.NONE):
        valid_moves.append(attack_right)

    # En passant
    if (position.equals(board.en_passant_target, attack_left)
            and (board.get_color(board.en_passant_target[0], board.en_passant_target[1])
            not in (color, Color.NONE))):
        valid_moves.append(board.en_passant_target)
    if (position.equals(board.en_passant_target, attack_right)
            and (board.get_color(board.en_passant_target[0], board.en_passant_target[1])
            not in (color, Color.NONE))):
        valid_moves.append(board.en_passant_target)

    # Remove moves that are now withing the bounds of the board
    i = 0
    while i < len(valid_moves):
        if (not position.is_in_bounds(valid_moves[i])
                or board.get_color(valid_moves[i][0], valid_moves[i][1]) == color):
            valid_moves.pop(i)
            i -= 1
        i += 1

    return valid_moves


def get_line_move(row: int, file: int, direction: list[int], board: typing.Any) -> list[list[int]]:
    """
    Returns all valid positions for piece at row and file in
    the direction of dir_row and dir_file
    For everystep in the line search we change row+=dir_row and file+=dir_file
    Returns 2d array of rows and files: [ [row,file], ... ]

    board has to be of type board.Board
    """

    color = board.get_color(row, file)

    valid_moves = []

    for i in range(1, 8):
        current_row = row + (direction[0] * i)
        current_file = file + (direction[1] * i)

        if not position.is_in_bounds([current_row, current_file]):
            break

        current_color = board.get_color(current_row, current_file)

        if current_color != color:
            valid_moves.append([current_row, current_file])

        if current_color != Color.NONE:
            break

    return valid_moves


def get_all_moves(color: Color, board: typing.Any, simulate: bool) -> tuple[list[list[int]], bool]:
    """
    Returns all valid moves for all pieces of a certain color
    Returns 2d array of rows and files: [ [row,file], ... ]
    Also returns true if the enemy king is in check, false if otherwise

    color has to be of type piece.Color
    board has to be of type board.Board
    """

    valid_moves = []
    enemy_in_check = False

    for row in range(0, 8):
        for file in range(0, 8):

            if board.get_color(row, file) != color:
                continue

            piece_moves = get_valid_moves(row, file, simulate, board)
            valid_moves.extend(piece_moves)

            # Check if we are checking the king
            for piece_move in piece_moves:
                if (board.get_color(piece_move[0], piece_move[1]) != color
                        and board.get_piece(piece_move[0], piece_move[1]) == Type.KING):
                    enemy_in_check = True

    return valid_moves, enemy_in_check


def piece_to_char(piece_type: Type, piece_color: Color) -> str:
    """
    Converts a piece to its corresponding character abreviation
    """

    result = "?"

    if piece_type == Type.PAWN:
        result = "P" if piece_color == Color.WHITE else "p"
    if piece_type == Type.KING:
        result = "K" if piece_color == Color.WHITE else "k"
    if piece_type == Type.QUEEN:
        result = "Q" if piece_color == Color.WHITE else "q"
    if piece_type == Type.ROOK:
        result = "R" if piece_color == Color.WHITE else "r"
    if piece_type == Type.KNIGHT:
        result = "N" if piece_color == Color.WHITE else "n"
    if piece_type == Type.BISHOP:
        result = "B" if piece_color == Color.WHITE else "b"

    return result


def char_to_piece(char: str) -> tuple[Type, Color]:
    """
    Converts a character to its corresponding piece type and color
    """

    piece_type = Type.NONE
    piece_color = Color.BLACK

    char = list(char)[0]

    if char.isupper():
        piece_color = Color.WHITE
        char = char.lower()

    if char == "p":
        piece_type = Type.PAWN
    if char == "q":
        piece_type = Type.QUEEN
    if char == "k":
        piece_type = Type.KING
    if char == "r":
        piece_type = Type.ROOK
    if char == "n":
        piece_type = Type.KNIGHT
    if char == "b":
        piece_type = Type.BISHOP

    if piece_type == Type.NONE:
        piece_color = Color.NONE

    return piece_type, piece_color
