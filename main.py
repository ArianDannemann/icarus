"""
The entry point for Icarus
"""

import board
import piece
import ui

board.promotion_target = piece.Type.QUEEN
#board.setup()
board.set_piece(0,4,piece.Type.KING,piece.Color.WHITE)
board.set_piece(0,7,piece.Type.ROOK,piece.Color.WHITE)
board.set_piece(0,0,piece.Type.ROOK,piece.Color.WHITE)
#board.set_piece(6,3,piece.Type.QUEEN,piece.Color.BLACK)
#board.set_piece(5,5,piece.Type.KNIGHT,piece.Color.WHITE)
board.set_piece(7,4,piece.Type.KING,piece.Color.BLACK)
board.set_piece(7,7,piece.Type.ROOK,piece.Color.BLACK)
board.set_piece(7,0,piece.Type.ROOK,piece.Color.BLACK)

ui.init()
ui.keep_alive()
