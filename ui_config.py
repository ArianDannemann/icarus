"""
Stores settings and references for the UI
(to make my linter happy)
"""

import tkinter as tk

title: str = "Icarus - v1.0.1"
white_color: str = "#7c6f64"
black_color: str = "#665c54"
select_color: str = "#458588"
flipped: bool = False

square_width: int = 80
square_height: int = 80

# --- REFERENCES ---
board_setup_frame: tk.Frame
game_info_frame: tk.Frame
fen_text: tk.StringVar
move_count_text: tk.Label
whos_turn_text: tk.Label
state_text: tk.Label
promotion_piece_text: tk.StringVar
