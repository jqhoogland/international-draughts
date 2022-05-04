from checkers.models import Move
from checkers.types import RowIndex, TileIndex, ColIndex
from checkers.utils import col_of, row_of


def is_x_rows_forward(move: Move, *, rows: int = 1) -> bool:
    return row_of(move.start) - row_of(move.end) == rows


def is_x_cols_away(move: Move, *, cols: int = 1) -> bool:
    return abs(col_of(move.start) - col_of(move.end)) == cols


def is_diagonal(move: Move) -> bool:
    return abs(col_of(move.start) - col_of(move.end)) == abs(row_of(move.start) - row_of(move.end))


def is_x_steps_on_diagonal(move: Move, *, steps: int = 1) -> bool:
    return is_x_rows_forward(move.start, move.end, rows=steps) and is_x_cols_away(move.start, move.end, cols=steps)


# Convenience aliases


def is_one_step_forward(move: Move) -> bool:
    return is_x_rows_forward(move.start, move.end, rows=1) and is_x_cols_away(move.start, move.end, cols=1)


def is_two_steps_forward(move: Move) -> bool:
    return is_x_rows_forward(move.start, move.end, rows=2) and is_x_cols_away(move.start, move.end, cols=2)


