from checkers.models import Board, PLAYER_ONE
from checkers.types import tilelist
from checkers.utils import tile_index_of, TileIndexError


def draw_grid(tiles: tilelist(str), *, width: int = 2):
    """A helper that prints a checkerboard that draws elements from ``tiles``
    to a board according to the international checkers standard tile ordering.

    (I.e.: Right-left, top-down starting in the second tile of the top row.)
    """

    board_repr = ""

    for i in range(10):
        board_repr += "|"
        for j in range(10):
            try:
                board_repr += f"{tiles[tile_index_of(i, j) - 1]}|"
            except TileIndexError:
                board_repr += " " * width + "|"

        board_repr += "\n"

    return board_repr


def draw_board(board: Board):
    piece_reprs = ["  "] * 50

    for i, player, is_king in sorted(board, key=lambda p: p.idx):
        if player is PLAYER_ONE:
            piece_reprs[i-1] = "X" + ("X" if is_king else "_")
        else:
            piece_reprs[i-1] = "O" + ("O" if is_king else "_")

    return draw_grid(piece_reprs, width=2)


def add_edges(board_repr: str):
    """Add labels to the edges of an board.

    .. NOTE:: This only works with width-2 grids.
    """

    top_indices = "  .  .01.  .02.  .03.  .04.  .05.\n"
    bottom_indices = "'46'  '47'  '48'  '49'  '50'  '"
    left_indices = "\n  \n06\n  \n16\n  \n26\n  \n36\n  \n46\n  \n  \n"
    right_indices = "\n  \n05  \n  \n15\n  \n25\n  \n35\n  \n45\n  \n  \n  \n"

    split_lines = zip(left_indices.split("\n"), \
                  (top_indices + board_repr + bottom_indices).split("\n"), \
                  right_indices.split("\n"))

    return '\n'.join([l + body + r for l, body, r in split_lines])


def draw_board_with_indices(board: Board):
    return add_edges(draw_board(board))


def draw_tile_indices():
    """A helper that prints a checkerboard with each tile noted by its
    official index (Because I cannot be bothered to memorize this &
    it acts as a test of :func:`tile_index_of` -- see below).
    """
    return draw_grid(list(str(i).zfill(2) for i in range(1, 51)))


if __name__ == "__main__":
    print(draw_tile_indices())

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

