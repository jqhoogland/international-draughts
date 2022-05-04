from typing import Optional

from checkers.models import Move, Board, Player
from checkers.types import RowIndex, TileIndex, ColIndex
from checkers.utils import col_of, row_of


def is_x_rows_forward(move: Move, *, rows: int = 1) -> bool:
    return row_of(move.start) - row_of(move.end) == rows


def is_x_rows_away(move: Move, *, rows: int = 1) -> bool:
    return abs(row_of(move.start) - row_of(move.end)) == rows


def is_x_cols_to_right(move: Move, *, cols: int = 1) -> bool:
    return col_of(move.start) - col_of(move.end) == cols


def is_x_cols_away(move: Move, *, cols: int = 1) -> bool:
    return abs(col_of(move.start) - col_of(move.end)) == cols


def is_diagonal(move: Move) -> bool:
    return abs(col_of(move.start) - col_of(move.end)) \
           == abs(row_of(move.start) - row_of(move.end))


def is_x_steps_on_diagonal(move: Move, *, steps: int = 1) -> bool:
    return is_x_rows_away(move, rows=steps) \
           and is_x_cols_away(move, cols=steps)


# Aliases for understandability


def is_one_step_forward(move: Move) -> bool:
    return is_x_rows_forward(move, rows=1) \
           and is_x_cols_away(move, cols=1)


def is_two_steps_away(move: Move) -> bool:
    return is_x_steps_on_diagonal(move, steps=2)


def is_occupied(board: Board, i: TileIndex, *, by: Optional[Player] = None) -> bool:
    """Check whether ``board`` has a piece at position ``i``.

    If ``by`` is included, additionally check whether that piece belongs to
    the player specified by this argument.
    """
    for (j, player, _) in board:
        if i == j and (not by or by == player):
            return True

    return False


# -- Single Moves
# All of these functions assume there is a valid piece in the starting position of move.

def is_valid_normal_step(board: Board, move: Move) -> bool:
    return is_one_step_forward(move) and not is_occupied(board, move.end)


def is_valid_normal_capture(board: Board, move: Move, player: Player) -> bool:
    return is_two_steps_away(move) \
           and is_occupied(board, move - 1, not player) \
           and not is_occupied(board, move.end)


def is_valid_normal_move(board: Board, move: Move, player: Player) -> bool:
    return is_valid_normal_step(board, move) \
           or is_valid_normal_capture(board, move, player)


def is_valid_king_step(board: Board, move: Move) -> bool:
    return is_diagonal(move) and all(map(lambda i: not is_occupied(board, i), move))


def is_valid_king_capture(board: Board, move: Move, player: Player) -> bool:
    return is_diagonal(move) \
           and all(map(lambda i: not is_occupied(board, i, by=player), move)) \
           and sum(map(lambda i: int(is_occupied(board, i, by=not player)), move)) == 1


def is_valid_king_move(board: Board, move: Move, player: Player) -> bool:
    return is_valid_king_step(board, move) \
           or is_valid_king_capture(board, move, player)


# -- Capture Series


def is_valid_normal_capture_series(board: Board, moves: list[Move], player: Player) -> bool:
    """Assumes moves is already validated for continuity. We keep track of a
    list of captured tiles for recursive calls to avoid capturing the same piece twice."""

    captured: list[TileIndex] = []

    for move in moves:
        if not is_valid_normal_capture(board, move, player) \
                or (capture := (move - 1).end) in captured:
            return False
        captured.append(capture)

    return True


def is_valid_king_capture_series(board: Board, moves: list[Move], player: Player) -> bool:
    captured: list[TileIndex] = []

    def get_capture(move: Move) -> TileIndex:
        return next(filter(lambda i: i in board.pieces, move))

    for move in moves:
        if not is_valid_king_capture(board, move, player) \
                or (capture := get_capture(move)) in captured:
            return False
        captured.append(capture)

    return True
