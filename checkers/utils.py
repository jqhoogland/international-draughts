import string

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
def col_of(i: TileIndex) -> ColIndex:
    # The corresponding value of i if shifted to one of the first two rows.
    i_normalized = ((i - 1) % 10)

    if i_normalized >= 5:
        return (i_normalized - 5) * 2

    return 1 + i_normalized * 2


@validate_arguments
def row_of(i: TileIndex) -> RowIndex:
    return (i - 1) // 5


def create_tile_indices_string():
    """A helper that prints a checkerboard with each tile noted by its
    official index (Because I cannot be bothered to memorize this &
    it acts as a test of :func:`tile_index_of`).
    """
    board_repr = ""

    for i in range(10):
        board_repr += "|"
        for j in range(10):
            try:
                board_repr += f"{str(tile_index_of(i, j)).zfill(2)}|"
            except TileIndexError:
                board_repr += "  |"

        board_repr += "\n"

    return board_repr


if __name__ == "__main__":

    # This is the test...
    print(create_tile_indices_string())

    # |  |01|  |02|  |03|  |04|  |05|
    # |06|  |07|  |08|  |09|  |10|  |
    # |  |11|  |12|  |13|  |14|  |15|
    # |16|  |17|  |18|  |19|  |20|  |
    # |  |21|  |22|  |23|  |24|  |25|
    # |26|  |27|  |28|  |29|  |30|  |
    # |  |31|  |32|  |33|  |34|  |35|
    # |36|  |37|  |38|  |39|  |40|  |
    # |  |41|  |42|  |43|  |44|  |45|
    # |46|  |47|  |48|  |49|  |50|  |
    
