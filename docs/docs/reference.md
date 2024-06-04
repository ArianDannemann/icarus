# Reference

Below you will find a list of the most importants methods of each class.

!!! tip

    This is by no means a complete list.
    The codebase is simple, try browsing around a bit!

## Board

### `setup`

=== "Parameters"

    None

=== "Description"

    Setup the board with the standard chess starting position.

=== "Usage"

    ```python
    import board

    my_board: board.Board = board.Board()
    my_board.setup()
    ```

### `move_piece`

=== "Parameters"

    - Input:
        - `row: int`, The current row of the piece you want to move
        - `file: int`, The current file of the piece you want to move
        - `new_row: int`, The row you want the piece to move to
        - `new_file: int`, The file you want the piece to move to
    - Output:
        - `True` if the move was legal and could be executed, `False` otherwise

=== "Description"

    Moves a piece according to standard chess rules.

    If you want to ignore rules and simply change the position of a piece, take a look at `teleport_piece`.

=== "Usage"

    The example belows plays the opening move *1. e4* for white.

    ```python
    import board

    my_board: board.Board = board.Board()
    my_board.setup()
    my_board.move_piece(1, 3, 3, 3)
    ```

### `teleport_piece`

=== "Parameters"

    - Input:
        - `row: int`, The current row of the piece you want to move
        - `file: int`, The current file of the piece you want to move
        - `new_row: int`, The row you want the piece to move to
        - `new_file: int`, The file you want the piece to move to

=== "Description"

    Similar to `move_piece` but will ignore all chess rules.

=== "Usage"

    The example belows will open the game by placing whites queens pawn on the square of the black queen, whiping it out in the process.

    This is illegal, since:

    - The pawn moves more than two spaces on the first move
    - The pawn takes in a direction other than a diagonal
    - The pawn moves over pieces
    - The pawn is now placed on the last row, without having been promoted

    ```python
    import board

    my_board: board.Board = board.Board()
    my_board.setup()
    my_board.teleport_piece(1, 3, 7, 3)
    ```

## Piece

tbd

## UI

tbd
