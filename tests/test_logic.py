"""

.. NOTE:: Some of these tests have ridiculous amounts of nested loops.
   That's gross. But it's not that bad when the maximum length per loop is 10.
   Also, code integrity is worth it.

   (This is hidden behind the handy ``itertools.product``.)

"""

import itertools
from contextlib import suppress

from checkers.utils import col_of, row_of, tile_index_of, TileIndexError
from checkers.rules import is_normal_move, is_x_rows_forward, is_x_cols_away


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
                assert is_x_rows_forward(tile_index_of(i2, j2), tile_index_of(i1, j1), rows=rows) \
                       == (rows == i2-i1)


def test_is_x_cols_away():
    for i1, j1, i2, j2 in itertools.product(*itertools.repeat(range(10), 4)):
        for cols in range(3):
            with suppress(TileIndexError):
                assert is_x_cols_away(tile_index_of(i2, j2), tile_index_of(i1, j1), cols=cols) \
                       == (cols == abs(j2-j1))


def test_cannot_move_normally_more_than_one_forward():
    pass


def test_cannot_move_normally_into_occupied_square():
    pass


def test_cannot_move_with_capture_into_occupied_square():
    pass


def test_cannot_move_normally_backwards():
    pass


def test_can_move_with_capture_backwards():
    pass
