"""
The entry point for Icarus
"""
# pylint: disable=unused-argument

import board
import piece
import ui

my_board: board.Board = board.Board()
my_board.promotion_target = piece.Type.QUEEN
my_board.setup()

my_ui: ui.UI = ui.UI()
my_ui.init(my_board)
my_ui.keep_alive()
