from checkers.domain.board import Board


def default_board() -> Board:
    return Board(list(range(31, 51)), list(range(1, 21)))