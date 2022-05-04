from dataclasses import dataclass
from typing import NamedTuple, Optional

from pydantic import conint, validate_arguments
from enum import Enum, Flag, auto

from checkers.types import TileIndex
from checkers.utils import col_of, row_of, tile_index_of


class Move(NamedTuple):
    start: TileIndex
    end: TileIndex

    def __add__(self, other: int) -> 'Move':
        """ Grow a move in the diagonal

        :param other:
        :return:
        """
        return Move(
            self.start,
            tile_index_of(
                row_of(self.end) + other,
                col_of(self.end) + other
            )
        )

    def __sub__(self, other: int) -> 'Move':
        return Move(
            self.start,
            tile_index_of(
                row_of(self.end) + other,
                col_of(self.end) + other
            )
        )


class Player(Enum):
    # More explicit than a bool.
    ONE = 1
    TWO = 2


class Tile(NamedTuple):
    idx: TileIndex
    player: Player
    is_king: bool


class BoardError(ValueError):
    pass


@dataclass(init=False)
class Board:
    tiles: list[Tile]

    @validate_arguments
    def __init__(self, p1: list[TileIndex], p2: list[TileIndex], *, kings: Optional[list[TileIndex]]):
        """
        Prepare a board by providing a list of indices of tiles for players 1 and 2.

        .. NOTE:: Here we see one of the benefits of using the international checkers
           standard indexing: we get validation right out of the box.

        To set up a standard game, check out the :func:`setup.default_board` factory.

        :param p1: Locations of player one's pieces.
        :param p2: Locations of player one's pieces.
        :param kings: Locations of both players' kings (if any).
        """
        if set(p1) & set(p2):
            raise BoardError("Cannot place two opposing tiles on the same square")

        kings = kings or []

        self.tiles = list(sorted(
            (*map(lambda i: Tile(i, p1, i in kings)),
             *map(lambda i: Tile(i, p2, i in kings))),
            key=lambda t: t.idx
        ))


