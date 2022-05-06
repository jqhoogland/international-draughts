import pytest

from checkers.logic.max_capture import is_max_capture, compute_max_capture
from checkers.models import Board, capture_series_to_moves, PLAYER_ONE, PLAYER_TWO
from checkers.utils.draw import draw_board_with_indices

@pytest.fixture()
def board_1():
    """
    .. code::

        .  .01.  .02.  .03.  .04.  .05.
        |  |[]|  |[]|  |[]|  |[]|  |[]|05
      06|[]|  |[]|  |[]|  |[]|  |[]|  |
        |  |[]|  |<>|  |<>|  |[]|  |[]|15
      16|[]|  |[]|  |[]|  |[]|  |[]|  |
        |  |[]|  |<>|  |[]|  |[]|  |[]|25
      26|[]|  |⊂⊃|  |⊂⊃|  |[]|  |[]|  |
        |  |[]|  |[]|  |[]|  |[]|  |[]|35
     36|[]|  |[]|  |[]|  |[]|  |[]|  |
       |  |[]|  |[]|  |[]|  |⊂⊃|  |[]|45
     46|[]|  |[]|  |[]|  |[]|  |[]|  |
       '46'  '47'  '48'  '49'  '50'  '

    """

    return Board([28, 44, 27], [22, 12, 13])


def test_max_capture_with_normal(board_1):
    p1_max_capture = compute_max_capture(board_1, PLAYER_ONE)
    assert p1_max_capture == 3
    
    p2_max_capture = compute_max_capture(board_1, PLAYER_TWO)
    assert p2_max_capture == 1
    

def test_is_max_capture(board_1):
    assert is_max_capture(board_1, capture_series_to_moves([28, 17, 8, 19]))
    assert not is_max_capture(board_1, capture_series_to_moves([28, 17, 8]))
    assert not is_max_capture(board_1, capture_series_to_moves([28, 17]))

    assert not is_max_capture(board_1, capture_series_to_moves([27, 18, 7]))
    assert not is_max_capture(board_1, capture_series_to_moves([27, 18, 9]))
    assert not is_max_capture(board_1, capture_series_to_moves([27, 18]))

    assert not is_max_capture(board_1, capture_series_to_moves([44, 40]))
    assert not is_max_capture(board_1, capture_series_to_moves([44, 39]))


@pytest.fixture()
def board_2():
    """
    .. code::

        .  .01.  .02.  .03.  .04.  .05.
        |  |[]|  |[]|  |[]|  |[]|  |[]|05
      06|[]|  |[]|  |[]|  |[]|  |[]|  |
        |  |[]|  |<>|  |[]|  |<>|  |[]|15
      16|[]|  |[]|  |[]|  |[]|  |[]|  |
        |  |[]|  |<>|  |[]|  |[]|  |[]|25
      26|[]|  |⊂⊃|  |⊂⊃|  |[]|  |[]|  |
        |  |[]|  |[]|  |[]|  |[]|  |[]|35
     36|[]|  |[]|  |[]|  |[]|  |[]|  |
       |  |[]|  |[]|  |[]|  |⊂⊃|  |[]|45
     46|[]|  |[]|  |[]|  |[]|  |[]|  |
       '46'  '47'  '48'  '49'  '50'  '

    """

    return Board([28, 44, 27], [22, 12, 14], kings=[28])


def test_max_capture_with_king(board_2):
    p1_max_capture = compute_max_capture(board_2, PLAYER_ONE)
    assert p1_max_capture == 3

    p2_max_capture = compute_max_capture(board_2, PLAYER_TWO)
    assert p2_max_capture == 1


def test_is_max_capture_with_king(board_2):
    assert is_max_capture(board_2, capture_series_to_moves([28, 17, 3, 20]))
    assert is_max_capture(board_2, capture_series_to_moves([28, 17, 3, 25]))
    assert not is_max_capture(board_2, capture_series_to_moves([28, 3, 20]))
    assert not is_max_capture(board_2, capture_series_to_moves([28, 17]))

    assert not is_max_capture(board_2, capture_series_to_moves([27, 18, 7]))
    assert not is_max_capture(board_2, capture_series_to_moves([27, 18]))

    assert not is_max_capture(board_2, capture_series_to_moves([44, 40]))
    assert not is_max_capture(board_2, capture_series_to_moves([44, 39]))
