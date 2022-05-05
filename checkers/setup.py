from checkers.models import Board


def default_board() -> Board:
    return Board(list(range(1, 20)), list(range(31, 51)))