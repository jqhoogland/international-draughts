from checkers.types import RowIndex, TileIndex, ColIndex
from checkers.utils import col_of, row_of


def is_x_rows_forward(start: TileIndex, end: TileIndex, *, rows: int = 1) -> bool:
    return row_of(start) - row_of(end) == rows


def is_x_cols_away(start: TileIndex, end: TileIndex, *, cols: int = 1) -> bool:
    return abs(col_of(start) - col_of(end)) == cols


def is_diagonal(start: TileIndex, end: TileIndex) -> bool:
    return abs(row_of(start) - row_of(end)) < 1


def is_normal_move(start: TileIndex, end: TileIndex) -> bool:
    return is_x_rows_forward(start, end, rows=1) and is_x_cols_away(start, end, cols=1)
