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

from checkers.models import Move, Board
from checkers.models.position import tile_index_of, TileIndexError
from checkers.logic.rules import is_x_rows_up, is_x_cols_away, is_diagonal, is_occupied, is_valid_normal_step, \
    is_valid_normal_capture


def test_is_forward():
    for i1, j1, i2, j2 in itertools.product(*itertools.repeat(range(10), 4)):
        for rows in range(3):
            with suppress(TileIndexError):
                assert is_x_rows_up(Move(tile_index_of(i2, j2), tile_index_of(i1, j1)), rows=rows) \
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


def test_is_occupied():
    p1 = [1, 5, 10, 20]
    p2 = [50, 45, 40, 30]
    empty = [i for i in range(1, 51) if i not in p1 and i not in p2]

    for p in p1:
        assert is_occupied(Board(p1, p2), p)

    for p in p2:
        assert is_occupied(Board(p1, p2), p)

    for p in empty:
        assert not is_occupied(Board(p1, p2), p)


def test_p1_is_valid_normal_step_if_empty():
    assert is_valid_normal_step(Board([28], []), Move(28, 22))
    assert is_valid_normal_step(Board([28], []), Move(28, 23))


def test_p1_is_not_valid_normal_step_if_backwards():
    assert not is_valid_normal_step(Board([28], []), Move(28, 33))
    assert not is_valid_normal_step(Board([28], []), Move(28, 32))


def test_p1_is_not_valid_normal_step_if_horizontal():
    assert not is_valid_normal_step(Board([28], []), Move(28, 37))
    assert not is_valid_normal_step(Board([28], []), Move(28, 29))


def test_p1_is_not_valid_normal_step_if_more_than_one():
    assert not is_valid_normal_step(Board([28], []), Move(28, 17))
    assert not is_valid_normal_step(Board([28], []), Move(28, 17))


def test_p1_is_not_valid_normal_step_if_occupied():
    assert not is_valid_normal_step(Board([28, 22], []), Move(28, 22))
    assert not is_valid_normal_step(Board([28], [23]), Move(28, 23))


def test_p1_is_valid_capture_if_end_is_empty():
    assert is_valid_normal_capture(Board([28], [22]), Move(28, 17))
    assert is_valid_normal_capture(Board([28], [23]), Move(28, 19))
    assert is_valid_normal_capture(Board([28], [33]), Move(28, 39))
    assert is_valid_normal_capture(Board([28], [32]), Move(28, 37))


def test_p1_is_not_valid_capture_if_jumping_own_piece():
    assert not is_valid_normal_capture(Board([28, 22], []), Move(28, 17))
    assert not is_valid_normal_capture(Board([28, 23], []), Move(28, 19))
    assert not is_valid_normal_capture(Board([28, 33], []), Move(28, 39))
    assert not is_valid_normal_capture(Board([28, 32], []), Move(28, 37))


def test_p1_is_not_valid_capture_if_end_is_occupied():
    assert not is_valid_normal_capture(Board([28, 17], [22]), Move(28, 17))
    assert not is_valid_normal_capture(Board([28], [23, 19]), Move(28, 19))
    assert not is_valid_normal_capture(Board([28, 39], [33]), Move(28, 39))
    assert not is_valid_normal_capture(Board([28], [32, 37]), Move(28, 37))


def test_p2_is_valid_normal_step_if_empty():
    assert is_valid_normal_step(Board([], [28]), Move(28, 33))
    assert is_valid_normal_step(Board([], [28]), Move(28, 32))


def test_p2_is_not_valid_normal_step_if_backwards():
    assert not is_valid_normal_step(Board([], [28]), Move(28, 22))
    assert not is_valid_normal_step(Board([], [28]), Move(28, 23))


def test_p2_is_not_valid_normal_step_if_horizontal():
    assert not is_valid_normal_step(Board([], [28]), Move(28, 37))
    assert not is_valid_normal_step(Board([], [28]), Move(28, 29))


def test_p2_is_not_valid_normal_step_if_more_than_one():
    assert not is_valid_normal_step(Board([], [28]), Move(28, 17))
    assert not is_valid_normal_step(Board([], [28]), Move(28, 17))


def test_p2_is_not_valid_normal_step_if_occupied():
    assert not is_valid_normal_step(Board([], [28, 22]), Move(28, 22))
    assert not is_valid_normal_step(Board([23], [28]), Move(28, 23))


def test_p2_is_valid_capture_if_end_is_empty():
    assert is_valid_normal_capture(Board([22], [28]), Move(28, 17))
    assert is_valid_normal_capture(Board([23], [28]), Move(28, 19))
    assert is_valid_normal_capture(Board([33], [28]), Move(28, 39))
    assert is_valid_normal_capture(Board([32], [28]), Move(28, 37))


def test_p2_is_not_valid_capture_if_jumping_own_piece():
    assert not is_valid_normal_capture(Board([], [28, 22]), Move(28, 17))
    assert not is_valid_normal_capture(Board([], [28, 23]), Move(28, 19))
    assert not is_valid_normal_capture(Board([], [28, 33]), Move(28, 39))
    assert not is_valid_normal_capture(Board([], [28, 32]), Move(28, 37))


def test_p2_is_not_valid_capture_if_end_is_occupied():
    assert not is_valid_normal_capture(Board([22], [28, 17]), Move(28, 17))
    assert not is_valid_normal_capture(Board([23, 19], [28]), Move(28, 19))
    assert not is_valid_normal_capture(Board([33], [28, 39]), Move(28, 39))
    assert not is_valid_normal_capture(Board([32, 37], [28]), Move(28, 37))

