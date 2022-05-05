import re
from dataclasses import dataclass
from typing import Optional

from pydantic import validate_arguments

from checkers.domain.move import Move, capture_series_to_moves
from checkers.domain.piece import Piece
from checkers.utils import TileIndex
from checkers.domain.player import PLAYER_ONE, PLAYER_TWO


class BoardError(ValueError):
    pass


class InvalidMoveFormat(ValueError):
    pass


@dataclass(init=False)
class Board:
    """Player one moves up. Player two moves down."""

    pieces: list[Piece]

    def _get_list_idx(self, idx: TileIndex) -> int:
        try:
            return next(filter(
                lambda i_p: i_p[1].idx == idx, enumerate(self.pieces)))[0]
        except StopIteration:
            raise IndexError(f"No tile with index '{idx}' found on board.") from None

    def pop(self, idx: TileIndex) -> Piece:
        """Remove and return the tile at the position ``idx``,
        according to international checkers notation, *not*
        the pythonic index of an element in ``pieces``.
        """
        return self.pieces.pop(self._get_list_idx(idx))

    def insert(self, tile: Piece):
        """Insert a ``tile`` at the position ``tile.idx``. See ``pop``"""
        try:
            i_end, _ = next(filter(
                lambda i_p: i_p[1].idx > tile.idx, enumerate(self.pieces)))

            self.pieces.insert(i_end, tile)
        except StopIteration:
            self.pieces.append(tile)

    def replace(self, p: Piece):
        """Insert a ``tile`` at the position ``tile.idx`` to replace an
        existing piece."""
        self.pop(p.idx)
        self.insert(p)

    def apply_step(self, move: Move) -> 'Board':
        """Apply the given step to a board, maintaining the list of pieces in
        the order of their notation.

        .. NOTE:: This assumes you've validated the move beforehand. It simply
           clears all of the tiles in the range of path.

        TODO: This defies immutability. Consider returning a new instance of
              Board instead.
        """
        starting_tile = self.pop(move.start)
        self.insert(Piece(move.end, starting_tile.player, starting_tile.is_king))

        return self

    def apply_captures(self, moves: list[Move]) -> 'Board':
        starting_tile = self.pop(moves[0].start)
        visited_idxs = [p for move in moves for p in move]
        self.pieces = [p for p in self.pieces if p.idx not in visited_idxs]
        self.insert(Piece(moves[-1].end, starting_tile.player, starting_tile.is_king))

        return self

    @validate_arguments
    def __init__(self, p1_pieces: list[TileIndex], p2_pieces: list[TileIndex], *,
                 kings: Optional[list[TileIndex]] = None):
        """
        Prepare a board by providing a list of indices of pieces for players 1 and 2.

        .. NOTE:: Here we see one of the benefits of using the international checkers
           standard indexing: we get validation right out of the box.

        To set up a standard game, check out the :func:`setup.default_board` factory.

        :param p1_pieces: Locations of player one's pieces.
        :param p2_pieces: Locations of player one's pieces.
        :param kings: Locations of both players' kings (if any).
        """
        if set(p1_pieces) & set(p2_pieces):
            raise BoardError("Cannot place two opposing pieces on the same square")

        kings = kings or []

        self.pieces = list(sorted(
            (*map(lambda i: Piece(i, PLAYER_ONE, i in kings), p1_pieces),
             *map(lambda i: Piece(i, PLAYER_TWO, i in kings), p2_pieces)),
            key=lambda t: t.idx
        ))

    def __iter__(self):
        return iter(self.pieces)

    def __getitem__(self, idx: TileIndex):
        return self.pieces[self._get_list_idx(idx)]

