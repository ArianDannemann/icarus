"""
The entry point for Icarus
"""

import board
import piece
import ui

board.promotion_target = piece.Type.QUEEN
board.setup()
#board.set_piece(3,3,piece.Type.KING,piece.Color.WHITE)
#board.set_piece(6,3,piece.Type.QUEEN,piece.Color.BLACK)
#board.set_piece(5,5,piece.Type.KNIGHT,piece.Color.WHITE)
#board.set_piece(3,5,piece.Type.ROOK,piece.Color.BLACK)

# TODO - there seems to be a bug where a pawn cant take a queen that is checking?
# (although that would reserve the check)

ui.init()
ui.keep_alive()
