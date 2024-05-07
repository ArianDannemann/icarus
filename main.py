"""
The entry point for Icarus
"""

from board import Board
import piece
import ui

board = Board()
board.promotion_target = piece.Type.QUEEN
board.setup()

ui.init()
ui.keep_alive()
