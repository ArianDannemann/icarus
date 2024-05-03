import board
import piece
import ui

#board.setup()
board.set_piece(3,3,piece.Type.BISHOP,piece.Color.WHITE)

ui.init()
ui.keep_alive()
