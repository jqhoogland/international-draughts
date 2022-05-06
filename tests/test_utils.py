
import itertools
from contextlib import suppress

from checkers.models.position import col_of, row_of, tile_index_of, TileIndexError


def test_tile_index_to_row_index():
    for i, j in itertools.product(*itertools.repeat(range(10), 2)):
        with suppress(TileIndexError):
            assert row_of(tile_index_of(i, j)) == i


def test_tile_index_to_col_index():
    for i, j in itertools.product(*itertools.repeat(range(10), 2)):
        with suppress(TileIndexError):
            assert col_of(tile_index_of(i, j)) == j