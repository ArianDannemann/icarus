import board
import piece

board.setup()
board.display()
board.set_piece(7,7,piece.Type.NONE,piece.Color.NONE)
board.set_piece(6,7,piece.Type.PAWN,piece.Color.WHITE)
board.promotion_target = piece.Type.QUEEN
result = board.move_piece(6,7,7,7)

board.display()
