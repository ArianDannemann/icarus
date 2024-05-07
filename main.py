"""
The entry point for Icarus
"""

import board
import piece
import ui

board.promotion_target = piece.Type.QUEEN
board.setup()

ui.init()
ui.keep_alive()
