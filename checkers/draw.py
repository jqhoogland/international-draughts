from checkers.types import tilelist
from checkers.utils import tile_index_of, TileIndexError


def draw_board(tiles: tilelist(str), *, width: int = 2):
    """A helper that prints a checkerboard that draws elements from ``tiles``
    to a board according to the international checkers standard tile ordering.

    (I.e.: Right-left, top-down starting in the second tile of the top row.)
    """

    board_repr = ""

    for i in range(10):
        board_repr += "|"
        for j in range(10):
            try:
                board_repr += f"{tiles(tile_index_of(i, j) - 1)}|"
            except TileIndexError:
                board_repr += " " * width + "|"

        board_repr += "\n"

    return board_repr


def create_tile_indices_string():
    """A helper that prints a checkerboard with each tile noted by its
    official index (Because I cannot be bothered to memorize this &
    it acts as a test of :func:`tile_index_of` -- see below).
    """
    return draw_board(list(i.zfill(2) for i in range(1, 51)))


if __name__ == "__main__":
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

