from typing import NamedTuple

from checkers.models.player import Player
from checkers.models.position import row_of, TileIndex


class Piece(NamedTuple):
    idx: TileIndex
    player: Player
    is_king: bool

    @property
    def has_reached_end(self) -> bool:
        return (self.player and row_of(self.idx) == 0) \
               or (not self.player and row_of(self.idx) == 9)

    def coronate(self) -> 'Piece':
        return Piece(self.idx, self.player, True)
