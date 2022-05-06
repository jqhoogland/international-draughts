from checkers.models import Piece, Board, PLAYER_ONE, PLAYER_TWO
from checkers.models.position import floor_tile_index_of


def test_board_contains():
    b = Board([28, 29, 15], [18, 1, 9], kings=[29, 1])

    for p in b._pieces:
        assert p in b
        assert p.idx in b


def test_board_pop():
    b = Board([28, 29, 15], [18, 1, 9], kings=[29, 1])

    assert b.pop(28) == Piece(28, PLAYER_ONE, False)
    assert b.pop(29) == Piece(29, PLAYER_ONE, True)
    assert b.pop(9) == Piece(9, PLAYER_TWO, False)

    assert b == Board([15], [18, 1], kings=[1])


def test_board_insert():
    b = Board([15], [18, 1], kings=[1])

    b.insert(Piece(28, PLAYER_ONE, False))
    b.insert(Piece(29, PLAYER_ONE, True))
    b.insert(Piece(9, PLAYER_TWO, False))

    assert b == Board([28, 29, 15], [18, 1, 9], kings=[29, 1])


def test_board_replace():
    b = Board([15], [18, 1], kings=[1])
    b.replace(Piece(15, PLAYER_TWO, True))

    assert b == Board([], [15, 18, 1], kings=[1, 15])


def test_crowning():
    assert Piece(1, PLAYER_ONE, False).coronate() == Piece(1, PLAYER_ONE, True)

    assert Piece(floor_tile_index_of(0, 5, direction=(0, 1)), PLAYER_ONE, False).has_reached_end
    assert not Piece(floor_tile_index_of(0, 5, direction=(0, 1)), PLAYER_TWO, False).has_reached_end
    assert all([not Piece(floor_tile_index_of(i, 5, direction=(1, 0)), PLAYER_ONE, False).has_reached_end for i in range(1, 9)])

    assert Piece(floor_tile_index_of(9, 5, direction=(0, 1)), PLAYER_TWO, False).has_reached_end
    assert not Piece(floor_tile_index_of(9, 5, direction=(0, 1)), PLAYER_ONE, False).has_reached_end
    assert all([not Piece(floor_tile_index_of(i, 5, direction=(-1, 0)), PLAYER_TWO, False).has_reached_end for i in range(0, 9)])