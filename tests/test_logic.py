"""

.. NOTE:: Some of these tests have ridiculous amounts of nested loops.
   That's gross. But it's not that bad when the maximum length per loop is 10.
   Also, code integrity is worth it.

   (This is hidden behind the handy ``itertools.product``.)

.. NOTE:: In retrospect, the movement (``is_forward``, ``is_x_cols_away``)
   aren't great (they're defined circularly).

"""

import itertools
from contextlib import suppress

from checkers.models import Move
from checkers.utils import col_of, row_of, tile_index_of, TileIndexError
from checkers.rules import is_x_rows_forward, is_x_cols_away, is_diagonal


def test_tile_index_to_row_index():
    for i, j in itertools.product(*itertools.repeat(range(10), 2)):
        with suppress(TileIndexError):
            assert row_of(tile_index_of(i, j)) == i


def test_tile_index_to_col_index():
    for i, j in itertools.product(*itertools.repeat(range(10), 2)):
        with suppress(TileIndexError):
            assert col_of(tile_index_of(i, j)) == j


def test_is_forward():
    for i1, j1, i2, j2 in itertools.product(*itertools.repeat(range(10), 4)):
        for rows in range(3):
            with suppress(TileIndexError):
                assert is_x_rows_forward(Move(tile_index_of(i2, j2), tile_index_of(i1, j1)), rows=rows) \
                       is (rows == i2-i1)


def test_is_x_cols_away():
    for i1, j1, i2, j2 in itertools.product(*itertools.repeat(range(10), 4)):
        for cols in range(3):
            with suppress(TileIndexError):
                assert is_x_cols_away(Move(tile_index_of(i2, j2), tile_index_of(i1, j1)), cols=cols) \
                       is (cols == abs(j2-j1))


def test_is_diagonal():
    for i1, j1, i2, j2 in itertools.product(*itertools.repeat(range(10), 4)):
        with suppress(TileIndexError):
            assert is_diagonal(Move(tile_index_of(i2, j2), tile_index_of(i1, j1))) \
                   is (abs(i1-i2) == abs(j1-j2))



def test_cannot_move_normally_into_occupied_square():
    pass


def test_cannot_move_with_capture_into_occupied_square():
    pass


def test_cannot_move_normally_backwards():
    pass


def test_can_move_with_capture_backwards():
    pass
