import board
import piece

board.setup()
board.display()

result = 0
for row in range(0, 2):
    for file in range(0, 8):
        temp = len(piece.get_valid_moves(row,file))
        result += temp

print(f"Result: {result}")
