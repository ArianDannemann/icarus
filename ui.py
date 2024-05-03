import tkinter as tk

import board
import piece

root = None
canvas = None

title = "Icarus"
white_color = "#9f90b0"
black_color = "#7d4a8d"

square_width = 80
square_height = 80

def init():
    """
    Initializes a tkinter window
    """

    global root
    global canvas

    root = tk.Tk()
    root.title(title)

    canvas = tk.Canvas(width=square_width*8, height=square_height*8)
    canvas.pack()

    root.bind("<Button 1>", click_square)

    update()

def update():
    """
    Draws all pieces to the current UI
    """

    global root
    global canvas

    for row in range(0, 8):
        for file in range(0, 8):

            color = white_color if (row + file) % 2 == 0 else black_color
            text = f"{board.get_color(7-row, file).name}\n{board.get_piece(7-row, file).name}"

            x = file * square_width
            y = row * square_height

            canvas.create_rectangle((x, y), (x+square_height, y+square_width), fill=color)

            if board.get_color(7-row, file) != piece.Color.NONE:
                canvas.create_text(x + square_width / 2, y + square_height / 2, text=text, fill="black")

def click_square(event_origin):
    """
    Handles mous click event
    """

    row, file = get_square()

    piece = board.get_piece(row, file)
    color = board.get_color(row, file)

    print(f"Clicked {color.name} {piece.name}")

def get_square():
    """
    Turns x and y of mouse click into row and file
    """

    x = root.winfo_pointerx() - root.winfo_rootx()
    y = root.winfo_pointery() - root.winfo_rooty()

    row = 7-int(y / square_height)
    file = int(x / square_width)

    return row, file

def keep_alive():
    global root

    root.mainloop()
