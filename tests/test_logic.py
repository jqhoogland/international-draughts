from contextlib import suppress

from checkers.utils import col_of, row_of, tile_index_of, TileIndexError
from checkers.rules import is_normal_move


def test_tile_index_to_row_index():
    for i in range(10):
        for j in range(10):
            with suppress(TileIndexError):
                assert row_of(tile_index_of(i, j)) == i


def test_tile_index_to_col_index():
    for i in range(10):
        for j in range(10):
            with suppress(TileIndexError):
                assert col_of(tile_index_of(i, j)) == j


def test_can_move_normally_one_forward():
    assert is_normal_move(27, 21)
    assert is_normal_move(27, 22)


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


