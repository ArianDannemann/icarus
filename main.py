import board
import piece

board.set_piece(3,3,piece.Type.KNIGHT,piece.Color.WHITE)

board.display()
print(f"Valid moves for knight: {len(piece.get_valid_moves(3,3))}")
