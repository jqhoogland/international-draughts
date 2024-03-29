from typing import Literal

from pydantic import validate_arguments
from pydantic.types import conint

RowIndex = conint(ge=0, lt=10)
ColIndex = conint(ge=0, lt=10)
TileIndex = conint(ge=1, le=50)


class TileIndexError(ValueError):
    pass


@validate_arguments
def tile_index_of(i: RowIndex, j: ColIndex) -> TileIndex:
    if (i + j) % 2 != 1:
        raise TileIndexError("The provided row and column index a non-playable (light) tile")

    return 1 + i * 5 + (j // 2)


@validate_arguments
def floor_tile_index_of(
        i: RowIndex, j: ColIndex,
        *, direction: tuple[Literal[1, 0, -1], Literal[1, 0, -1]]) -> TileIndex:
    """Unlike ``tile_index_of``, fallback to an adjacent tile if we specify a
    non-playable (light) tile. Which adjacent tile is specified by ``direction``."""

    if (i + j) % 2 != 1:
        return 1 + ((i + direction[0]) * 5) + ((j + direction[1]) // 2)

    return 1 + i * 5 + (j // 2)


@validate_arguments
def row_of(i: TileIndex) -> RowIndex:
    return (i - 1) // 5


@validate_arguments
def col_of(i: TileIndex) -> ColIndex:
    # The value of i as if shifted to one of the first two rows.
    i_normalized = ((i - 1) % 10)

    if i_normalized >= 5:
        return (i_normalized - 5) * 2

    return 1 + i_normalized * 2


def row_col_of(i: TileIndex) -> tuple[RowIndex, ColIndex]:
    return row_of(i), col_of(i)


def move_r(i: TileIndex, cols: int) -> TileIndex:
    return tile_index_of(row_of(i), col_of(i) + cols)


def move_u(i: TileIndex, rows: int) -> TileIndex:
    return tile_index_of(row_of(i) - rows, col_of(i))


def move_ur(i: TileIndex, diag: int) -> TileIndex:
    return tile_index_of(row_of(i) - diag, col_of(i) + diag)


def move_dr(i: TileIndex, diag: int) -> TileIndex:
    return tile_index_of(row_of(i) + diag, col_of(i) + diag)
