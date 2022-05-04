from pydantic import validate_arguments

from checkers.types import ColIndex, RowIndex, TileIndex


class TileIndexError(ValueError):
    pass


@validate_arguments
def tile_index_of(i: RowIndex, j: ColIndex) -> TileIndex:
    if (i + j) % 2 != 1:
        raise TileIndexError("The provided row and column index a non-playable (light) tile")

    return 1 + i * 5 + (j // 2)


@validate_arguments
def row_of(i: TileIndex) -> RowIndex:
    return (i - 1) // 5


@validate_arguments
def col_of(i: TileIndex) -> ColIndex:
    # The corresponding value of i if shifted to one of the first two rows.
    i_normalized = ((i - 1) % 10)

    if i_normalized >= 5:
        return (i_normalized - 5) * 2

    return 1 + i_normalized * 2


def row_col_of(i: TileIndex) -> tuple[RowIndex, ColIndex]:
    return row_of(i), col_of(i)
