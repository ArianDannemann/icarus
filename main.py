"""
The entry point for Icarus
"""
# pylint: disable=unused-argument

import board
import piece
import ui

board = board.Board()
board.promotion_target = piece.Type.QUEEN
board.setup()

ui = ui.UI()
ui.init(board)
ui.keep_alive()
