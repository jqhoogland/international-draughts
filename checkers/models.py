from dataclasses import dataclass
from typing import NamedTuple, Optional, Literal, Iterator

from pydantic import validate_arguments

from checkers.types import TileIndex
from checkers.utils import col_of, row_of, tile_index_of


class Move(NamedTuple):
    start: TileIndex
    end: TileIndex

    @property
    def direction(self) -> tuple[Literal[1, -1], Literal[1, -1]]:
        """To compute the "direction" of a move, we treat ``start`` as the origin
        and determine what quadrant ``end`` is in."""

        quadrant_unnormed = (row_of(self.end) - row_of(self.start),
                             col_of(self.end) - col_of(self.start))
        return (quadrant_unnormed[0] / abs(quadrant_unnormed[0]),
                quadrant_unnormed[1] / abs(quadrant_unnormed[1]))

    def __add__(self, other: int) -> 'Move':
        """This is a bit of python magic that lets us override the standard
        ``+`` operation. In this case, we define adding an int to a move as
        extending the move in the direction of the diagonal pointing from
        start to end.

        (This assumes that this a well-formed move.)
        """

        direction = self.direction

        return Move(
            self.start,
            tile_index_of(
                row_of(self.end) + direction[0] * other,
                col_of(self.end) + direction[1] * other
            )
        )

    def __sub__(self, other: int) -> 'Move':
        """See ``__add__``. Subtraction is defined analogously but in the
        direction opposite the move."""

        direction = self.direction

        return Move(
            self.start,
            tile_index_of(
                row_of(self.end) - direction[0] * other,
                col_of(self.end) - direction[1] * other
            )
        )

    def __iter__(self) -> Iterator[TileIndex]:
        """Returns an iterator over all of the tile indices encountered during this
        move, not including ``start`` but including ``end``. """

        direction = self.direction

        step = Move(
            self.start,
            tile_index_of(
                row_of(self.end) + direction[0],
                col_of(self.end) + direction[1]
            )
        )

        yield step.end

        while row_of(step.end) <= row_of(self.end) and col_of(step.end) <= col_of(self.end):
            step = step + 1
            yield step.end


PLAYER_ONE = True
PLAYER_TWO = False

Player = Literal[PLAYER_ONE, PLAYER_TWO]  # I.e. bool (just a tad more explicit).


class Tile(NamedTuple):
    idx: TileIndex
    player: Player
    is_king: bool


class BoardError(ValueError):
    pass


@dataclass(init=False)
class Board:
    pieces: list[Tile]

    def pop(self, idx: TileIndex) -> Tile:
        """Remove and return the tile at the position ``idx``,
        according to international checkers notation, *not*
        the pythonic index of an element in ``pieces``.
        """

        i_start, _ = next(enumerate(filter(
            lambda p: p.idx == idx, self.pieces)))

        return self.pieces.pop(i_start)

    def insert(self, tile: Tile):
        """Insert a ``tile`` at the position ``tile.idx``. See ``pop``"""
        i_end, _ = next(enumerate(filter(
            lambda p: p.idx > tile.idx, self.pieces)))

        self.pieces.insert(i_end, tile)

    def apply_move(self, move: Move) -> 'Board':
        """Apply the given move to a board, maintaining the list of pieces in
        the order of their notation.

        .. NOTE:: This assumes you've validated the move beforehand. It simply
           clears all of the tiles in the range of path.

        TODO: This defies immutability. Consider returning a new instance of
              Board instead.
        """
        starting_tile = self.pop(move.start)
        self.pieces = [p for p in self.pieces if p.idx not in move]
        self.insert(Tile(move.end, starting_tile.player, starting_tile.is_king))

        return self

    def apply_all(self, moves: list[Move]) -> 'Board':
        pass

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
            (*map(lambda i: Tile(i, PLAYER_ONE, i in kings), p1_pieces),
             *map(lambda i: Tile(i, PLAYER_TWO, i in kings), p2_pieces)),
            key=lambda t: t.idx
        ))

    def __iter__(self):
        return iter(self.pieces)
