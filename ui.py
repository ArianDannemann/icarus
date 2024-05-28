
"""
Holds the UI class
"""

import typing
import tkinter as tk
from PIL import Image, ImageTk

import piece
from exceptions import InconsistentState


class UI():
    """
    Icarus user interface
    """

    root: tk.Tk
    canvas: tk.Canvas
    board: typing.Any
    board_setup_frame: tk.Frame
    game_info_frame: tk.Frame
    fen_text: tk.StringVar
    move_count_text: tk.Label
    whos_turn_text: tk.Label

    title: str = "Icarus"
    white_color: str = "#7c6f64"
    black_color: str = "#665c54"
    select_color: str = "#458588"
    flipped: bool = False

    square_width: int = 80
    square_height: int = 80

    selected_piece: list[int] = [-1, -1]
    selected_moves: list[list[int]] = []

    piece_images: list[ImageTk.PhotoImage] = []

    def init(self, board: typing.Any) -> None:
        """
        Initializes a tkinter window
        """

        # Setup TK root
        self.root = tk.Tk()
        self.root["bg"] = "#262626"
        self.root.title(self.title)

        # Create the board canvas and bind left click
        self.canvas = tk.Canvas(width=self.square_width * 8, height=self.square_height * 8)
        self.canvas.config(highlightthickness=0)
        self.board = board
        self.root.bind("<Button 1>", self.click_square)

        # Create the UI
        self.canvas.grid(row=0, rowspan=2, column=0)

        # Load the first frame to the right of the board
        self.load_setup_board_frame()
        self.load_settings_choose_frame()

        # Prepare the other menus
        self.load_game_info_frame()
        self.game_info_frame.destroy()

        # Start loading the board and pieces themself
        self.load_piece_images()
        self.update()

    def load_settings_choose_frame(self) -> None:
        """
        Loads and displays the "choose settings" page
        """

        clicked = tk.StringVar()
        clicked.set("Board setup")
        settings_dropdown = tk.OptionMenu(
            self.root,
            clicked,
            "Board setup",
            "Game info",
            command=self.handle_settings_dropdown
        )
        settings_dropdown.config(
            bg="#4e4e4e",
            fg="#ebdbb2",
            borderwidth=0,
            width=20,
            highlightthickness=0,
            activebackground="#ebdbb2",
            activeforeground="#4e4e4e",
            font=("Monospace Regular", 12)
        )
        settings_dropdown["menu"].config(
            bg="#4e4e4e",
            fg="#ebdbb2",
            borderwidth=0,
            activebackground="#ebdbb2",
            activeforeground="#4e4e4e",
            font=("Monospace Regular", 12)
        )

        settings_dropdown.grid(row=0, column=1, sticky="n")

    def load_setup_board_frame(self) -> None:
        """
        Loads and displays the setup board settings page
        """

        # Board setup frame
        self.board_setup_frame = tk.Frame(self.root)

        self.fen_text = tk.StringVar(value="unset")
        fen_entry_box = tk.Entry(self.board_setup_frame, textvariable=self.fen_text)

        load_fen_button = tk.Button(
            self.board_setup_frame,
            text="Load FEN",
            command=self.handle_load_fen_button
        )
        load_fen_button.config(
            bg="#4e4e4e",
            fg="#ebdbb2",
            borderwidth=0,
            highlightthickness=0,
            activebackground="#ebdbb2",
            activeforeground="#4e4e4e",
            font=("Monospace Regular", 12)
        )

        fen_entry_box.config(
            bg="#4e4e4e",
            fg="#ebdbb2",
            borderwidth=0,
            highlightthickness=0,
            font=("Monospace Regular", 12),
        )

        flip_board_button = tk.Button(
            self.board_setup_frame,
            text="Flip board",
            command=self.handle_flip_board_button
        )
        flip_board_button.config(
            bg="#4e4e4e",
            fg="#ebdbb2",
            borderwidth=0,
            highlightthickness=0,
            activebackground="#ebdbb2",
            activeforeground="#4e4e4e",
            font=("Monospace Regular", 12)
        )

        self.board_setup_frame.grid(row=1, column=1, sticky="new")
        fen_entry_box.pack(anchor="n", fill="x")
        load_fen_button.pack(anchor="n", fill="x")
        flip_board_button.pack(anchor="n", fill="x")

    def load_game_info_frame(self) -> None:
        """
        Loads and displays the game info settings page
        """

        # Board setup frame
        self.game_info_frame = tk.Frame(self.root)

        self.move_count_text = tk.Label(self.game_info_frame, text="Turn 0")
        self.whos_turn_text = tk.Label(self.game_info_frame, text="WHITE has the turn")

        self.move_count_text.config(
            bg="#262626",
            fg="#ebdbb2",
            borderwidth=0,
            highlightthickness=0,
            font=("Monospace Regular", 12)
        )
        self.whos_turn_text.config(
            bg="#262627",
            fg="#ebdbb2",
            borderwidth=0,
            highlightthickness=0,
            font=("Monospace Regular", 12)
        )

        self.game_info_frame.grid(row=1, column=1, sticky="new")
        self.whos_turn_text.pack(anchor="n", fill="x")
        self.move_count_text.pack(anchor="n", fill="x")

    def update(self) -> None:
        """
        Draws all pieces to the current UI
        """

        self.canvas.delete("all")
        self.fen_text.set(self.board.board_to_fen())

        if self.game_info_frame.winfo_exists() == 1:
            self.whos_turn_text.config(text=f"{self.board.active_color.name} has the turn")
            self.move_count_text.config(text=f"Turn {int(self.board.active_turn/2)}")

        for row in range(0, 8):
            for file in range(0, 8):

                color = self.white_color if (row + file) % 2 == 0 else self.black_color

                # Take the flipped board into account
                display_row = 7 - row if not self.flipped else row
                display_file = file if not self.flipped else 7 - file

                # Check if square is movable
                for selected_move in self.selected_moves:
                    if selected_move[0] == display_row and selected_move[1] == display_file:

                        color = self.select_color

                x = file * self.square_width
                y = row * self.square_height

                # Create the background square
                self.canvas.create_rectangle(
                    (x, y),
                    (x + self.square_height, y + self.square_width),
                    fill=color
                )

                # Draw the piece
                if self.board.get_color(display_row, display_file) != piece.Color.NONE:
                    current_piece = self.board.get_piece(display_row, display_file)
                    current_color = self.board.get_color(display_row, display_file)

                    if current_piece.value == 0 and current_color.value != 0:
                        raise InconsistentState("Piece is NONE but color is set")
                    if current_piece.value != 0 and current_color.value == 0:
                        raise InconsistentState("Color is NONE but piece is set")

                    self.canvas.create_image(
                        x,
                        y,
                        anchor=tk.NW,
                        image=self.get_piece_image(current_piece, current_color)
                    )

    def get_piece_image(self,
                        current_piece: piece.Type,
                        current_color: piece.Color) -> ImageTk.PhotoImage | None:
        """
        Gets the corresponding image to a piece of color
        """

        if current_color == piece.Color.WHITE:
            return self.piece_images[current_piece.value - 1]

        if current_color == piece.Color.BLACK:
            return self.piece_images[(current_piece.value - 1) + 6]

        return None

    def load_piece_images(self) -> None:
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

    def load_piece_image(self, name: str) -> ImageTk.PhotoImage:
        """
        Loads a single piece image from resources/pieces/ into memory
        """

        return ImageTk.PhotoImage(
            Image.open(f"./resources/pieces/{name}.png").resize(
                (self.square_width, self.square_height)
            ).convert("RGBA")
        )

    def click_square(self, event_origin: typing.Any) -> None:
        """
        Handles mous click event

        event_origin is a tkinter event
        """

        # NOTE - required since pylint does not like unused vars
        # (it is unused because we use absolute x and why, however
        # the event still needs to pass it)
        _ = event_origin

        row, file = self.get_square()

        # Take flipped board into consideration
        row = row if not self.flipped else 7 - row
        file = file if not self.flipped else 7 - file

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

    def get_square(self) -> tuple[int, int]:
        """
        Turns x and y of mouse click into row and file
        """

        x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        y = self.root.winfo_pointery() - self.root.winfo_rooty()

        row = 7 - int(y / self.square_height)
        file = int(x / self.square_width)

        return row, file

    def keep_alive(self) -> None:
        """
        Runs the mainloop of the root window
        """

        self.root.mainloop()

    def handle_load_fen_button(self) -> None:
        """
        Called when the "Load FEN" button is pressed
        """

        self.board.load_fen(self.fen_text.get())
        self.update()

    def handle_flip_board_button(self) -> None:
        """
        Called when the "Flip board" button is pressed
        """

        self.flipped = not self.flipped
        self.update()

    def handle_settings_dropdown(self, event: typing.Any) -> None:
        """
        Called when something was selected from the settings dropdown
        """

        self.board_setup_frame.destroy()
        self.game_info_frame.destroy()

        if event == "Board setup":
            self.load_setup_board_frame()
        elif event == "Game info":
            self.load_game_info_frame()

        self.update()
