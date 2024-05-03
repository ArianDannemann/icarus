import board
import piece

board.set_piece(0,0,piece.Type.KING,piece.Color.WHITE)

board.display()
print(f"Valid moves for king: {len(piece.get_valid_moves(0,0))}")
