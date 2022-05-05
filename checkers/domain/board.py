import re
from dataclasses import dataclass
from typing import NamedTuple, Optional

from pydantic import validate_arguments
from pydantic.types import conint

from checkers.domain.move import Move, capture_series_to_moves
from checkers.domain.player import PLAYER_ONE, PLAYER_TWO, Player


TileIndex = conint(ge=1, le=50)


class Piece(NamedTuple):
    idx: TileIndex
    player: Player
    is_king: bool


class BoardError(ValueError):
    pass


class InvalidMoveFormat(ValueError):
    pass


@dataclass(init=False)
class Board:
    pieces: list[Piece]

    def pop(self, idx: TileIndex) -> Piece:
        """Remove and return the tile at the position ``idx``,
        according to international checkers notation, *not*
        the pythonic index of an element in ``pieces``.
        """

        i_start, _ = next(enumerate(filter(
            lambda p: p.idx == idx, self.pieces)))

        return self.pieces.pop(i_start)

    def insert(self, tile: Piece):
        """Insert a ``tile`` at the position ``tile.idx``. See ``pop``"""
        i_end, _ = next(enumerate(filter(
            lambda p: p.idx > tile.idx, self.pieces)))

        self.pieces.insert(i_end, tile)

    def apply_step(self, move: Move) -> 'Board':
        """Apply the given step to a board, maintaining the list of pieces in
        the order of their notation.

        .. NOTE:: This assumes you've validated the move beforehand. It simply
           clears all of the tiles in the range of path.

        TODO: This defies immutability. Consider returning a new instance of
              Board instead.
        """
        starting_tile = self.pop(move.start)
        self.pieces = [p for p in self.pieces if p.idx not in move]
        self.insert(Piece(move.end, starting_tile.player, starting_tile.is_king))

        return self

    def apply_captures(self, moves: list[Move]) -> 'Board':
        starting_tile = self.pop(moves[0].start)
        visited_idxs = [p for move in moves for p in move]
        self.pieces = [p for p in self.pieces if p.idx not in visited_idxs]
        self.insert(Piece(moves[-1].end, starting_tile.player, starting_tile.is_king))

        return self

    def apply(self, cmd: str):
        if match := re.search(r"(\d{1,2})\-(\d{1,2})", cmd):
            start, end = match.group(1), match.group(2)
            move = Move(int(start), int(end))

            # TODO: Validation
            return self.apply_step(move)

        elif idxs := list(map(int, cmd.split("x"))):
            # TODO: Validation
            moves = capture_series_to_moves(idxs)
            return self.apply_captures(moves)
            
        raise InvalidMoveFormat(f"Couldn't parse the given move '{cmd}'")

    @validate_arguments
    def __init__(self, p1_pieces: list[TileIndex], p2_pieces: list[TileIndex], *, kings: Optional[list[TileIndex]] = None):
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
