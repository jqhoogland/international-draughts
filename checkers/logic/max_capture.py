"""
The most conceptually difficult part is right here: In international draughts
you have to make the move that yields the most captures.

So we have to compute what the maximum number of captures to validate moves.

The secret is in the data structure:

- A collection of pieces whose moves we have not yet computed.
- The maximum capture series length encountered thusfar.

(We don't actually care for what the particular path is, only how long it is.)

"""
import functools
import itertools
import warnings
from typing import Callable, Iterable

from pydantic import ValidationError

from checkers.logic.rules import get_valid_normal_capture, get_valid_king_capture
from checkers.models import Board, Player, Move, TileIndex
from checkers.models.position import move_ur, move_dr, TileIndexError, move_u, move_r


def get_normal_moves():
    return itertools.product((move_ur, move_dr), (2, -2))


def get_king_moves():
    return itertools.product((move_ur, move_dr, move_u, move_r),
                             itertools.chain(range(-11, 0), range(1, 11)))


def _generate_captures(
        get_tiles: Callable[[], Iterable[TileIndex]],
        get_valid_capture: Callable[[Board, Move, Player], bool],
        board: Board,
        start: TileIndex,
        player: Player,
) -> list[TileIndex]:
    for move, amt in get_tiles():
        try:
            end = move(start, amt)
            if capture := get_valid_capture(board, Move(start, end), player=player):
                yield end, capture

        except (TileIndexError, ValidationError):
            pass


_generate_normal_captures = functools.partial(_generate_captures, get_normal_moves, get_valid_normal_capture)
_generate_king_captures = functools.partial(_generate_captures, get_king_moves, get_valid_king_capture)


def _compute_max_capture_abstract(
        get_next_idxs: Callable[[Board, TileIndex, Player], list[TileIndex]],
        board: Board,
        idx: TileIndex,
        captured: list[TileIndex] = None,
        max_capture: int = 0,
        player: Player = None
):
    """
    :param get_next_idxs: How to find the next indices (this is the difference
                          between kings and non-kings)
    :param board:
    :param idx:
    :param captured: A list of already captured pieces (so we don't end up in
                    loops)
    :param max_capture: The maximum path length encountered so far.
    """
    captured = captured or []
    _max_capture = max_capture

    for next_idx, newly_captured in get_next_idxs(board, idx, player):
        if newly_captured in captured:
            continue

        max_capture = max(
            max_capture,
            _compute_max_capture_abstract(
                get_next_idxs,
                board,
                next_idx,
                captured=[*captured, newly_captured],
                max_capture=_max_capture + 1,
                player=player
            )
        )

    return max_capture


_compute_normal_max_capture = functools.partial(_compute_max_capture_abstract,
                                                _generate_normal_captures)
_compute_king_max_capture = functools.partial(_compute_max_capture_abstract,
                                              _generate_king_captures)


def compute_max_capture(board: Board, player: Player) -> int:
    max_capture = 0

    for p in board:
        if p.player is not player:
            continue

        _compute_max_capture = _compute_king_max_capture \
            if p.is_king \
            else _compute_normal_max_capture

        max_capture = max(max_capture, _compute_max_capture(board, p.idx, player=player))

    return max_capture


def is_max_capture(board: Board, moves: list[Move]) -> bool:
    return len(moves) == compute_max_capture(board, board[moves[0].start].player)


def validate_max_capture(board: Board, moves: list[Move]):
    max_capture = compute_max_capture(board, board[moves[0].start].player)
    is_maximal = len(moves) == max_capture

    if not is_maximal:
        # This isn't perfect and still allows pieces to jump onto other pieces,
        # but I'm happy for now.
        warnings.warn(f"{moves} is not maximal ({max_capture}).")
