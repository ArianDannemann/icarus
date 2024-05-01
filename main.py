import board
import piece

board.setup()
#board.display()

result = board.move_piece(1,3,3,3)
result += board.move_piece(3,3,4,3)
result += board.move_piece(6,4,4,4)
result += board.move_piece(4,3,5,4)
result += board.move_piece(5,4,6,5)
board.promotion_target = piece.Type.QUEEN
board.move_piece(6,5,7,6)

board.display()
print(f"Playerd {result} moves")
