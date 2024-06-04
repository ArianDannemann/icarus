# Getting started

## Installing dependencies

Below is a list of all dependencies, how to install them and why we need them:

- Tkinter, `pip install tk`, used for the graphical user interface
- PIL, `pip install Pillow`, used to load images for the chess pieces
- typing, `pip install typing`, used to provide typing information
- Mkdocs, `apt install mkdocs`, used to generate our documentation
- Mkdocs material theme, `pip install mkdocs-material`, theme for the documentation

Alternatively, you can run `bash scripts/install_dependencies.sh` from the root directory.

!!! note

    This will only install dependencies necessary to *run* the app.
    If you want to build the documentation, you will need to install the needed dependencies from the list above.

## Setting up a board

In order to setup a board, we will need to import the `board` class:

```python
import board
```

We can then create a local instance of a board.
This means Icarus supports multiple games being played at once on different boards:

```python
my_board: board.Board = board.Board()
```

And finally place pieces in the standard chess starting position:

```python
my_board.setup()
```

## Displaying the board

=== "In the console"

    Since we have already created our board, we can used its own `display` method to print it to the console:

    ```python
    my_board.display()
    ```

=== "In the GUI"

    In order to display our board in a GUI, we need to create an instance of the `UI` class:

    ```python
    import ui

    my_ui: ui.UI = ui.UI()
    my_ui.init(my_board)
    my_ui.keep_alive()
    ```

    !!! note

        `UI.keep_alive()` runs the main loop of the Tk "root" widget.
        Without this, the GUI would show up once and immediatly disappear again.
