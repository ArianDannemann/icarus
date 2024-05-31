![Pylint workflow](https://github.com/ArianDannemann/icarus/actions/workflows/pylint.yml/badge.svg)
![Mypy workflow](https://github.com/ArianDannemann/icarus/actions/workflows/lint.yml/badge.svg)
![PEP8 workflow](https://github.com/ArianDannemann/icarus/actions/workflows/pep8.yml/badge.svg)

<p align="center">
  <img src="logo/logo.png" width="350" title="Icarus Logo" atl="logo">
</p>

# Icarus

Simple python chess application with UI

## Screenshots

<p align="center">
  <img src="logo/icarus-v1.0.0.png" title="Screenshot" atl="logo">
</p>

## Usage

You can setup a board with UI like this:

```python
import board
import ui

my_board: board.Board = board.Board()
# Pleace pieces in standard chess starting position
my_board.setup()

my_ui: ui.UI = ui.UI()
my_ui.init(my_board)
my_ui.keep_alive()
```
