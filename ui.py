
"""
Holds the UI class
"""

import tkinter as tk
from PIL import Image, ImageTk

import piece


class UI():
    """
    Icarus user interface
    """

    root = None
    canvas = None
    board = None

    title = "Icarus"
    white_color = "#9f90b0"
    black_color = "#7d4a8d"
    select_color = "#0000ff"

    square_width = 80
    square_height = 80

    selected_piece: list[int] = [-1, -1]
    selected_moves: list[list[int]] = []

    piece_images: list[ImageTk.PhotoImage] = []

    def init(self, board):
        """
        Initializes a tkinter window
        """

        self.root = tk.Tk()
        self.root.title(self.title)

        self.canvas = tk.Canvas(width=self.square_width * 8, height=self.square_height * 8)
        self.canvas.pack()

        self.board = board
        self.root.bind("<Button 1>", self.click_square)

        self.load_piece_images()
        self.update()

    def update(self):
        """
        Draws all pieces to the current UI
        """

        self.canvas.delete("all")

        for row in range(0, 8):
            for file in range(0, 8):

                color = self.white_color if (row + file) % 2 == 0 else self.black_color

                # Check if square is movable
                for selected_move in self.selected_moves:
                    if selected_move[0] == 7 - row and selected_move[1] == file:

                        color = self.select_color

                x = file * self.square_width
                y = row * self.square_height

                self.canvas.create_rectangle(
                    (x, y),
                    (x + self.square_height, y + self.square_width),
                    fill=color
                )

                if self.board.get_color(7 - row, file) != piece.Color.NONE:
                    self.canvas.create_image(
                        x,
                        y,
                        anchor=tk.NW,
                        image=self.get_piece_image(
                            self.board.get_piece(7 - row, file),
                            self.board.get_color(7 - row, file)
                        )
                    )

    def get_piece_image(self, current_piece, current_color):
        """
        Gets the corresponding image to a piece of color
        """

        if current_color == piece.Color.WHITE:
            return self.piece_images[current_piece.value - 1]

        if current_color == piece.Color.BLACK:
            return self.piece_images[(current_piece.value - 1) + 6]

        return None

    def load_piece_images(self):
        """
        Pre-loads alls piece images into memory
        """

        self.piece_images.append(self.load_piece_image("w_p"))
        self.piece_images.append(self.load_piece_image("w_k"))
        self.piece_images.append(self.load_piece_image("w_q"))
        self.piece_images.append(self.load_piece_image("w_r"))
        self.piece_images.append(self.load_piece_image("w_b"))
        self.piece_images.append(self.load_piece_image("w_n"))
        self.piece_images.append(self.load_piece_image("b_p"))
        self.piece_images.append(self.load_piece_image("b_k"))
        self.piece_images.append(self.load_piece_image("b_q"))
        self.piece_images.append(self.load_piece_image("b_r"))
        self.piece_images.append(self.load_piece_image("b_b"))
        self.piece_images.append(self.load_piece_image("b_n"))

    def load_piece_image(self, name):
        """
        Loads a single piece image from resources/pieces/ into memory
        """

        return ImageTk.PhotoImage(
            Image.open(f"./resources/pieces/{name}.png").resize(
                (self.square_width, self.square_height)
            ).convert("RGBA")
        )

    def click_square(self, event_origin):
        """
        Handles mous click event
        """

        # NOTE - required since pylint does not like unused vars
        # (it is unused because we use absolute x and why, however
        # the event still needs to pass it)
        _ = event_origin

        row, file = self.get_square()

        current_piece = self.board.get_piece(row, file)

        if self.selected_piece[0] != -1:
            result = self.board.move_piece(
                self.selected_piece[0],
                self.selected_piece[1],
                row,
                file
            )
            self.selected_piece = [-1, -1]
            self.selected_moves = []

            self.update()

            if result:
                return

        if current_piece != piece.Type.NONE:
            self.selected_piece = [row, file]
            self.selected_moves = piece.get_valid_moves(row, file, True, self.board)

            self.update()

    def get_square(self):
        """
        Turns x and y of mouse click into row and file
        """

        x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        y = self.root.winfo_pointery() - self.root.winfo_rooty()

        row = 7 - int(y / self.square_height)
        file = int(x / self.square_width)

        return row, file

    def keep_alive(self):
        """
        Runs the mainloop of the root window
        """

        self.root.mainloop()
