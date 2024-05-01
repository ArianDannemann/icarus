import board
import piece

board.set_piece(0,0,piece.Type.BISHOP,piece.Color.WHITE)
board.move_piece(0,0,7,7)

board.display()
