"""
Hold the class Board
"""

import piece
import position


class Board():
    """
    Handles piece positioning and moving on a board
    """

    board = [0] * 64
    color = [0] * 64

    en_passant_target = [-1, -1]
    en_passant_victim = [-1, -1]
    en_passant_valid = False

    # 0: king moved, 1 if yes
    # 1: a rook moved, 1 if yes
    # 2: h rook moved, 1 if yes
    white_castle_info = [0, 0, 0]
    black_castle_info = [0, 0, 0]

    promotion_target = piece.Type.NONE

    def setup(self):
        """
        Sets up the default chess position
        """

        self.set_piece(0, 0, piece.Type.ROOK, piece.Color.WHITE)
        self.set_piece(0, 1, piece.Type.KNIGHT, piece.Color.WHITE)
        self.set_piece(0, 2, piece.Type.BISHOP, piece.Color.WHITE)
        self.set_piece(0, 3, piece.Type.QUEEN, piece.Color.WHITE)
        self.set_piece(0, 4, piece.Type.KING, piece.Color.WHITE)
        self.set_piece(0, 5, piece.Type.BISHOP, piece.Color.WHITE)
        self.set_piece(0, 6, piece.Type.KNIGHT, piece.Color.WHITE)
        self.set_piece(0, 7, piece.Type.ROOK, piece.Color.WHITE)
        self.set_piece(1, 0, piece.Type.PAWN, piece.Color.WHITE)
        self.set_piece(1, 1, piece.Type.PAWN, piece.Color.WHITE)
        self.set_piece(1, 2, piece.Type.PAWN, piece.Color.WHITE)
        self.set_piece(1, 3, piece.Type.PAWN, piece.Color.WHITE)
        self.set_piece(1, 4, piece.Type.PAWN, piece.Color.WHITE)
        self.set_piece(1, 5, piece.Type.PAWN, piece.Color.WHITE)
        self.set_piece(1, 6, piece.Type.PAWN, piece.Color.WHITE)
        self.set_piece(1, 7, piece.Type.PAWN, piece.Color.WHITE)

        self.set_piece(7, 0, piece.Type.ROOK, piece.Color.BLACK)
        self.set_piece(7, 1, piece.Type.KNIGHT, piece.Color.BLACK)
        self.set_piece(7, 2, piece.Type.BISHOP, piece.Color.BLACK)
        self.set_piece(7, 3, piece.Type.QUEEN, piece.Color.BLACK)
        self.set_piece(7, 4, piece.Type.KING, piece.Color.BLACK)
        self.set_piece(7, 5, piece.Type.BISHOP, piece.Color.BLACK)
        self.set_piece(7, 6, piece.Type.KNIGHT, piece.Color.BLACK)
        self.set_piece(7, 7, piece.Type.ROOK, piece.Color.BLACK)
        self.set_piece(6, 0, piece.Type.PAWN, piece.Color.BLACK)
        self.set_piece(6, 1, piece.Type.PAWN, piece.Color.BLACK)
        self.set_piece(6, 2, piece.Type.PAWN, piece.Color.BLACK)
        self.set_piece(6, 3, piece.Type.PAWN, piece.Color.BLACK)
        self.set_piece(6, 4, piece.Type.PAWN, piece.Color.BLACK)
        self.set_piece(6, 5, piece.Type.PAWN, piece.Color.BLACK)
        self.set_piece(6, 6, piece.Type.PAWN, piece.Color.BLACK)
        self.set_piece(6, 7, piece.Type.PAWN, piece.Color.BLACK)

    def display(self):
        """
        Print the current board layout to console
        """

        print("")
        for row in range(7, -1, -1):
            print(f" {row}:  ", end="")
            for file in range(0, 8):
                piece_type = self.get_piece(row, file)
                piece_color = self.get_color(row, file)

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

    def get_piece(self, row, file):
        """
        Returns the piece at row and file
        """

        if row > 7 or row < 0 or file > 7 or file < 0:
            return piece.Type.NONE

        return piece.Type(self.board[(row*8) + file])

    def set_piece(self, row, file, piece_type=piece.Type.PAWN, piece_color=piece.Color.WHITE):
        """
        Sets piece at row and file to type
        """

        if row > 7 or row < 0 or file > 7 or file < 0:
            return

        self.board[(row*8) + file] = piece_type.value
        self.set_color(row, file, piece_color)

    def get_color(self, row, file):
        """
        Gets color of piece at row and file
        """

        if not position.is_in_bounds([row, file]):
            return piece.Color.NONE

        return piece.Color(self.color[(row*8) + file])

    def set_color(self, row, file, new_color):
        """
        Sets color of piece at row and file to color
        """

        if not position.is_in_bounds([row, file]):
            return

        self.color[(row*8) + file] = new_color.value

    def teleport_piece(self, row, file, new_row, new_file):
        """
        Teleports piece from row and file to new_row and new_file
        while ignoring all chess rules
        """

        self.set_piece(
                new_row,
                new_file,
                piece.Type(self.get_piece(row, file)),
                piece.Color(self.get_color(row, file))
        )
        self.set_piece(row, file, piece.Type.NONE, piece.Color.NONE)

    def move_piece(self, row, file, new_row, new_file):
        """
        Moves piece from row and file to new_row and new_file
        according to chess rules
        Returns 1 if move was legal, 0 otherwise
        """

        result = 0
        found_en_passant = False

        current_piece = self.get_piece(row, file)
        current_color = self.get_color(row, file)

        for valid_move in piece.get_valid_moves(row, file, True, self):
            if position.equals(valid_move, [new_row, new_file]):

                self.teleport_piece(row, file, new_row, new_file)

                found_en_passant = self.handle_en_passant(row, new_row, new_file, current_piece)

                # Check for promotion
                if (current_piece == piece.Type.PAWN and new_row in [0, 7]):
                    self.set_piece(
                            new_row,
                            new_file,
                            self.promotion_target,
                            self.get_color(new_row, new_file)
                    )

                # Castle
                if current_piece == piece.Type.KING and abs(file-new_file) > 1:
                    if new_file > file:
                        self.teleport_piece(row, 7, row, 5)
                    else:
                        self.teleport_piece(row, 0, row, 3)

                # Update castling information
                castle_info = self.black_castle_info
                if current_color == piece.Color.WHITE:
                    castle_info = self.white_castle_info

                if current_piece == piece.Type.KING:
                    castle_info[0] = 1
                elif current_piece == piece.Type.ROOK and file == 0:
                    castle_info[1] = 1
                elif current_piece == piece.Type.ROOK and file == 7:
                    castle_info[2] = 1

                result = 1
                break

        self.en_passant_valid = (result == 1 and found_en_passant)
        if not self.en_passant_valid:
            self.en_passant_target = [-1, -1]

        return result

    def handle_en_passant(self, row, new_row, new_file, current_piece):
        """
        Subroutine of move_piece
        Checks all piece related things considering en passant
        Return True if en passant can be played the next move
        """

        # Check if en passant was done
        if (current_piece == piece.Type.PAWN
                and position.equals(self.en_passant_target, [new_row, new_file])
                and self.en_passant_valid):
            print("en passant")
            self.set_piece(
                    self.en_passant_victim[0],
                    self.en_passant_victim[1],
                    piece.Type.NONE,
                    piece.Color.NONE
            )

        # Check if en passant can be done in the next move
        if current_piece == piece.Type.PAWN and abs(row-new_row) > 1:
            self.en_passant_target = (
                [new_row-1, new_file]
                if self.get_color(new_row, new_file) == piece.Color.WHITE else
                [new_row+1, new_file]
            )
            self.en_passant_victim = ([new_row, new_file])
            return True

        return False

    def copy(self):
        """
        Returns a copy of board and color arrays
        """

        return self.board.copy(), self.color.copy()
