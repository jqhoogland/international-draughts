"""
These functions are undertested because they've already effectively been tested
in practice via the modules in :mod:`checkers.io`.
"""

from dataclasses import dataclass

from pydantic.types import conlist

from checkers.models import Board, PLAYER_ONE
from checkers.models.position import tile_index_of, TileIndexError
from checkers.utils.stringx import center_multiline


@dataclass(frozen=True)
class DrawOptions:
    """Options to control how the board is rendered.

    .. NOTE:: It's generally good to use immutable data, but especially if you
       want to include instances of this class as a default.
    """
    p1_normal = "⊂⊃"
    p1_king = "⊆⊇"

    p2_normal = "<>"
    p2_king = "≤≥"

    light_empty = "  "
    dark_empty = "[]"


default_draw_options = DrawOptions()


def draw_grid(tiles: conlist(str, min_items=50, max_items=50), options: DrawOptions = default_draw_options):
    """A helper that prints a checkerboard that draws elements from ``tiles``
    to a board according to the international checkers standard tile ordering.

    (I.e.: Indexes only dark tiles right-to-left, top-down starting in the
    second tile of the top row.)
    """

    board_repr = ""

    for i in range(10):
        board_repr += "|"
        for j in range(10):
            try:
                board_repr += f"{tiles[tile_index_of(i, j) - 1]}|"
            except TileIndexError:
                board_repr += options.light_empty + "|"

        board_repr += "\n"

    return board_repr


def draw_board(board: Board, options: DrawOptions = default_draw_options):
    piece_reprs = [options.dark_empty] * 50

    for i, player, is_king in sorted(board, key=lambda p: p.idx):
        if player is PLAYER_ONE:
            piece_reprs[i - 1] = options.p1_king if is_king else options.p1_normal
        else:
            piece_reprs[i - 1] = options.p2_king if is_king else options.p2_normal

    return draw_grid(piece_reprs, options=options)


def add_edges(board_repr: str):
    """Adds labels indicating the standard international draughts index label
    of edges squares to a checkerboard.

    Hardwired & a bit gross, but unquestionably faster than trying to
    prematurely optimize.
    """

    top_indices = " .  .01.  .02.  .03.  .04.  .05. \n "
    bottom_indices = "'46'  '47'  '48'  '49'  '50'  '"
    left_indices = "\n  \n06\n  \n16\n  \n26\n  \n36\n  \n46\n  \n  \n"
    right_indices = "\n05  \n  \n15\n  \n25\n  \n35\n  \n45\n  \n  \n  \n  \n"

    split_lines = zip(left_indices.split("\n"),
                      (top_indices + board_repr + bottom_indices).split("\n"),
                      right_indices.split("\n"))

    return '\n'.join([l + body + r for l, body, r in split_lines])


def draw_board_with_indices(board: Board, options: DrawOptions = default_draw_options):
    return add_edges(draw_board(board, options=options))


def draw_centered_board_with_indices(board: Board, char: str = " ", width: int = 80, options: DrawOptions = default_draw_options):
    return center_multiline(draw_board_with_indices(board, options=options), char=char, width=width)


def draw_tile_indices(options: DrawOptions = default_draw_options):
    """A helper that prints a checkerboard with each tile noted by its
    official index (Because I cannot be bothered to memorize this &
    it acts as a test of :func:`tile_index_of` -- see below).
    """
    return draw_grid(list(str(i).zfill(2) for i in range(1, 51)), options=options)


