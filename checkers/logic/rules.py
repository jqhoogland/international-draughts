"""
This could use a bit of a refactor:
- Instead of predicate tests, raise InvalidMoveError's so you can provide
  players more informative feedback.
- Many of these should be "private" (as close as you can get with Python)
- Possibly, group them together into a ``Rules`` class. That said, I prefer
  leaning towards excess functional programming over excess OO.

"""
from typing import Optional

from checkers.models import Move, Board, Player
from checkers.models.move import InvalidMoveError
from checkers.models.position import col_of, row_of, TileIndex
from checkers.utils.itertoolsx import first, first_index


def is_x_rows_up(move: Move, *, rows: int = 1) -> bool:
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


def is_perp(move: Move) -> bool:
    return col_of(move.start) == col_of(move.end) \
           or row_of(move.start) == row_of(move.end)


def is_x_steps_on_diagonal(move: Move, *, steps: int = 1) -> bool:
    return is_x_rows_away(move, rows=steps) \
           and is_x_cols_away(move, cols=steps)


# Aliases for understandability


def is_one_step_forward(board: Board, move: Move) -> bool:
    direction = 1 if board[move.start].player else -1

    return is_x_rows_up(move, rows=direction) \
           and is_x_cols_away(move, cols=1)


def is_two_steps_away(move: Move) -> bool:
    return is_x_steps_on_diagonal(move, steps=2)


def is_occupied(board: Board, i: TileIndex, *, by: Optional[Player] = None) -> bool:
    """Check whether ``board`` has a piece at position ``i``.

    If ``by`` is included, additionally check whether that piece belongs to
    the player specified by this argument.
    """
    for (j, player, _) in board:
        if i == j and (by is None or by == player):
            return True

    return False


# -- Single Moves
# All of these functions assume there is a valid piece in the starting position of move.

def is_valid_normal_step(board: Board, move: Move) -> bool:
    return is_one_step_forward(board, move) and not is_occupied(board, move.end)


def is_valid_normal_capture(board: Board, move: Move, *, player: Optional[Player] = None) -> bool:
    if player is None:
        player = board[move.start].player

    return is_two_steps_away(move) \
           and is_occupied(board, (move - 1).end, by=not player) \
           and not is_occupied(board, move.end)


def get_valid_normal_capture(board: Board, move: Move, *, player: Optional[Player] = None) -> TileIndex:
    return is_valid_normal_capture(board, move, player=player) and (move - 1).end


def is_valid_king_step(board: Board, move: Move) -> bool:
    return (is_diagonal(move) or is_perp(move)) \
           and all(map(lambda i: not is_occupied(board, i) or i == move.start, move))


def is_valid_king_capture(board: Board, move: Move, *, player: Optional[Player] = None) -> bool:
    if player is None:
        player = board[move.start].player

    return (is_diagonal(move) or is_perp(move) and not is_occupied(board, move.end)) \
           and all(map(lambda i: not is_occupied(board, i, by=player) or i == move.start, move)) \
           and sum(map(lambda i: int(is_occupied(board, i, by=not player)), move)) == 1


def get_valid_king_capture(board: Board, move: Move, *, player: Optional[Player] = None) -> TileIndex:
    return is_valid_king_capture(board, move, player=player) \
           and first(lambda i: is_occupied(board, i, by=not player), move)


# -- Capture Series


def is_valid_normal_capture_series(board: Board, moves: list[Move]) -> bool:
    """Assumes moves is already validated for continuity. We keep track of a
    list of captured tiles for recursive calls to avoid capturing the same piece twice.

    Does not check that this capture series is maximal.
    """
    captured: list[TileIndex] = []

    for move in moves:
        if not is_valid_normal_capture(board, move, player=board[moves[0].start].player) \
                or (capture := (move - 1).end) in captured:
            yield False
        captured.append(capture)
        yield True


def is_valid_king_capture_series(board: Board, moves: list[Move]) -> bool:
    """See ``is_valid_normal_capture_series``.
    Does not check that this capture series is maximal.
    """
    captured: list[TileIndex] = []

    def get_capture(move: Move) -> TileIndex:
        idxs = (p.idx for p in board)
        try:
            return next(filter(lambda i: i in idxs, move))
        except StopIteration:
            yield False

    for move in moves:
        if not is_valid_king_capture(board, move, player=board[moves[0].start].player) \
                or (capture := get_capture(move)) in captured:
            yield False
        captured.append(capture)

        yield True


def is_valid_step(board: Board, move: Move):
    return is_valid_king_step(board, move) \
        if board[move.start].is_king \
        else is_valid_normal_step(board, move)


def validate_step(board: Board, move: Move):
    if not is_valid_step(board, move):
        raise InvalidMoveError(f"'({move.start}, {move.end})' is not a valid step.")


def _is_valid_capture_series(board: Board, moves: list[Move]):
    return (is_valid_king_capture_series(board, moves)
            if board[moves[0].start].is_king
            else is_valid_normal_capture_series(board, moves))


def is_valid_capture_series(board: Board, moves: list[Move]):
    return all(_is_valid_capture_series(board, moves))


def get_invalid_capture(board: Board, moves: list[Move]) -> Move:
    return moves[first_index(lambda e: not e, _is_valid_capture_series(board, moves))]


def validate_captures(board: Board, moves: list[Move]):
    if not is_valid_capture_series(board, moves):
        move = get_invalid_capture(board, moves)

        raise InvalidMoveError(f"'({move.start}, {move.end})' is not a valid step.")
