import tkinter as tk

import board
import piece

root = None

title = "Icarus"
white_color = "#9f90b0"
black_color = "#7d4a8d"

def init():
    """
    Initializes a tkinter window
    """

    global root

    root = tk.Tk()
    root.title(title)

    update()

def update():
    """
    Draws all pieces to the current UI
    """

    global root

    for row in range(0, 8):
        for file in range(0, 8):

            color = white_color if (row + file) % 2 == 0 else black_color


            text = f"{board.get_color(7-row, file).name}\n{board.get_piece(7-row, file).name}"

            if board.get_color(7-row, file) == piece.Color.NONE:
                square = tk.Label(root, bg=color, width=10, height=4, borderwidth=0, relief="solid")
            else:
                square = tk.Label(root, text=text, bg=color, width=10, height=4, borderwidth=0, relief="solid")

            square.grid(row=row, column=file)

def keep_alive():
    global root

    root.mainloop()
