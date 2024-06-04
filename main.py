"""
The entry point for Icarus
"""
# pylint: disable=unused-argument

import board
import ui

my_board: board.Board = board.Board()
my_board.setup()

my_ui: ui.UI = ui.UI()
my_ui.init(my_board)
my_ui.keep_alive()
