from abc import ABC
from collections.abc import Collection
from dataclasses import dataclass
from typing import Optional, Iterator

from pydantic import validate_arguments

from checkers.models.move import Move
from checkers.models.piece import Piece
from checkers.models.player import PLAYER_ONE, PLAYER_TWO
from checkers.models.position import TileIndex
from checkers.utils.itertoolsx import first, first_index


class BoardError(ValueError):
    pass


class InvalidMoveError(ValueError):
    pass


class Board(Collection):
    """Board is a collection for pieces, where pieces are indexed according to
    their position in standard international draughts format.

    (For reference: Player one moves up. Player two moves down.)

    TODO: This defies immutability. Consider making this immutable (such that
          the provided methods return new instances).
    """
    _pieces: list[Piece]

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

        self._pieces = list(sorted(
            (*map(lambda i: Piece(i, PLAYER_ONE, i in kings), p1_pieces),
             *map(lambda i: Piece(i, PLAYER_TWO, i in kings), p2_pieces)),
            key=lambda t: t.idx
        ))

    def apply_step(self, move: Move) -> 'Board':
        """Apply the given step to a board, maintaining the list of pieces in
        the order of their notation.

        .. NOTE:: This assumes you've validated the move beforehand. It simply
           clears all of the tiles in the range of path.
        """
        self.insert(
            self.pop(move.start)
                .position(move.end)
        )

        return self

    def apply_captures(self, moves: list[Move]) -> 'Board':
        """Apply a (series of) capture(s) to the board.

        .. NOTE:: This assumes you've validated the moves beforehand (also for
           continuity). It simply clears all of the tiles in the range of path.
        """

        starting_tile = self.pop(moves[0].start)
        visited_idxs = [i for move in moves for i in move]
        self._pieces = [p for p in self if p.idx not in visited_idxs]
        self.insert(starting_tile.position(moves[-1].end))

        return self

    # -- Methods inspired by list() -------------------------------------------

    def _get_list_idx(self, idx: TileIndex) -> int:
        ls_idx = first_index(lambda p: p.idx == idx, self)

        if ls_idx == -1:
            raise IndexError(f"No tile with index '{idx}' found on board.") from None

        return ls_idx

    def pop(self, idx: TileIndex) -> Piece:
        """Remove and return the tile at the position ``idx``,
        according to international checkers notation, *not*
        the pythonic index of an element in ``pieces``.
        """
        return self._pieces.pop(self._get_list_idx(idx))

    def insert(self, tile: Piece):
        """Insert a ``tile`` at the position ``tile.idx``. See ``pop``"""
        ls_idx = first_index(lambda p: p.idx > tile.idx, self)

        if ls_idx == -1:
            return self._pieces.append(tile)

        return self._pieces.insert(ls_idx, tile)

    def replace(self, p: Piece):
        """Insert a ``tile`` at the position ``tile.idx`` to replace an
        existing piece."""
        self.pop(p.idx)
        self.insert(p)

    # -- Methods to satisfy Collection ----------------------------------------

    def __len__(self) -> int:
        return len(self._pieces)

    def __iter__(self) -> Iterator[Piece]:
        return iter(self._pieces)

    def __getitem__(self, idx: TileIndex) -> Piece:
        return self._pieces[self._get_list_idx(idx)]

    def __contains__(self, tile: TileIndex) -> bool:
        try:
            return self[tile.idx] == tile
        except IndexError:
            return False

    def __eq__(self, other: 'Board') -> bool:
        return self._pieces == other._pieces

    def __hash__(self):
        return hash(tuple(self._pieces))  # _pieces is always ordered