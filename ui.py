"""
Icarus user interface
"""

import tkinter as tk
from PIL import Image, ImageTk

import board
import piece

root = None
canvas = None

title = "Icarus"
white_color = "#9f90b0"
black_color = "#7d4a8d"
select_color = "#0000ff"

square_width = 80
square_height = 80

selected_piece = [-1,-1]
selected_moves = []

piece_images = []

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

    load_piece_images()
    update()

def update():
    """
    Draws all pieces to the current UI
    """

    global root
    global canvas
    global selected_moves
    global piece_images

    canvas.delete("all")

    for row in range(0, 8):
        for file in range(0, 8):

            color = white_color if (row + file) % 2 == 0 else black_color
            text = f"{board.get_color(7-row, file).name}\n{board.get_piece(7-row, file).name}"

            # Check if square is movable
            for selected_move in selected_moves:
                if selected_move[0] == 7-row and selected_move[1] == file:
                    color = select_color

            x = file * square_width
            y = row * square_height

            canvas.create_rectangle((x, y), (x+square_height, y+square_width), fill=color)

            if board.get_color(7-row, file) != piece.Color.NONE:
                #canvas.create_text(x + square_width / 2, y + square_height / 2, text=text, fill="black")
                canvas.create_image(
                        x,
                        y,
                        anchor=tk.NW,
                        image=get_piece_image(
                            board.get_piece(7-row, file),
                            board.get_color(7-row, file)
                        )
                )

def get_piece_image(current_piece, current_color):
    """
    Gets the corresponding image to a piece of color
    """

    global piece_images

    if current_color == piece.Color.WHITE:
        return piece_images[current_piece.value-1]
    elif current_color == piece.Color.BLACK:
        return piece_images[(current_piece.value-1)+6]

def load_piece_images():
    """
    Pre-loads alls piece images into memory
    """

    global piece_images

    piece_images.append(load_piece_image("w_p"))
    piece_images.append(load_piece_image("w_k"))
    piece_images.append(load_piece_image("w_q"))
    piece_images.append(load_piece_image("w_r"))
    piece_images.append(load_piece_image("w_b"))
    piece_images.append(load_piece_image("w_n"))
    piece_images.append(load_piece_image("b_p"))
    piece_images.append(load_piece_image("b_k"))
    piece_images.append(load_piece_image("b_q"))
    piece_images.append(load_piece_image("b_r"))
    piece_images.append(load_piece_image("b_b"))
    piece_images.append(load_piece_image("b_n"))

def load_piece_image(name):
    """
    Loads a single piece image from resources/pieces/ into memory
    """

    return ImageTk.PhotoImage(Image.open(f"./resources/pieces/{name}.png").resize((square_width, square_height)).convert("RGBA"))

def click_square(event_origin):
    """
    Handles mous click event
    """

    global selected_piece
    global selected_moves

    row, file = get_square()

    current_piece = board.get_piece(row, file)
    color = board.get_color(row, file)

    if (selected_piece[0] != -1):
        result = board.move_piece(selected_piece[0], selected_piece[1], row, file)
        selected_piece = [-1,-1]
        selected_moves = []

        update()

        if result:
            return

    if (current_piece != piece.Type.NONE):
        selected_piece = [row, file]
        selected_moves = piece.get_valid_moves(row,file)

        update()

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
