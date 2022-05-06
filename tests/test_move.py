from checkers.models import Board, Move


def test_move_addition():
    assert Move(18, 12) + 1 == Move(18, 7)
    assert Move(18, 13) + 1 == Move(18, 9)
    assert Move(18, 23) + 1 == Move(18, 29)
    assert Move(18, 22) + 1 == Move(18, 27)


def test_move_subraction():
    assert Move(18, 7) - 1 == Move(18, 12)
    assert Move(18, 9) - 1 == Move(18, 13)
    assert Move(18, 29) - 1 == Move(18, 23)
    assert Move(18, 27) - 1 == Move(18, 22)


def test_move_floor_division():
    assert Move(18, 7) // 2 == Move(18, 12)
    assert Move(18, 1) // 3 == Move(18, 12)
    assert Move(32, 14) // 2 == Move(32, 23)


def test_move_len():
    assert len(Move(18, 12)) == 1
    assert len(Move(18, 7)) == 2
    assert len(Move(47, 24)) == 5


def test_iter_move():
    assert tuple(Move(46, 5)) == (46, 41, 37, 32, 28, 23, 19, 14, 10, 5)
    assert tuple(Move(5, 46)) == tuple(reversed((46, 41, 37, 32, 28, 23, 19, 14, 10, 5)))
    assert tuple(Move(1, 45)) == (1, 7, 12, 18, 23, 29, 34, 40, 45)
    assert tuple(Move(45, 1)) == tuple(reversed((1, 7, 12, 18, 23, 29, 34, 40, 45)))


def test_normal_step():
    assert Board([32], []).apply_step(Move(32, 28)) == Board([28], [])
    assert Board([32], []).apply_step(Move(32, 27)) == Board([27], [])


def test_king_step():
    assert Board([32], [], kings=[32]).apply_step(Move(32, 5)) == Board([5], [], kings=[5])
    assert Board([32], [], kings=[32]).apply_step(Move(32, 16)) == Board([16], [], kings=[16])


def test_normal_capture():
    assert Board([32], [28]).apply_captures([Move(32, 23)]) == Board([23], [])
    assert Board([32], [27, 28]).apply_captures([Move(32, 16)]) == Board([16], [28])


def test_king_capture():
    assert Board([32], [28], kings=[32]).apply_captures([Move(32, 5)]) == Board([5], [], kings=[5])
    assert Board([32, 45], [38, 5], kings=[32]).apply_captures([Move(32, 43)]) == Board([43, 45], [5], kings=[43])
    assert Board([32, 45, 15], [37, 5, 16], kings=[32]).apply_captures([Move(32, 46)]) == Board([46, 45, 15], [5, 16], kings=[46])


def test_normal_captures():
    assert False


def test_king_captures():
    assert False

