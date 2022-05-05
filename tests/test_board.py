from checkers.domain import Piece, Board, PLAYER_ONE, PLAYER_TWO


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

