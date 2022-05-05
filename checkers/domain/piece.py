from typing import NamedTuple

from pydantic.types import conint

from checkers.domain.player import Player

TileIndex = conint(ge=1, le=50)


class Piece(NamedTuple):
    idx: TileIndex
    player: Player
    is_king: bool