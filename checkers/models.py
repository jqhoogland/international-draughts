from dataclasses import dataclass
from typing import NamedTuple

from pydantic import conint
from enum import Enum

from checkers.types import TileIndex


class Move(NamedTuple):
    start: TileIndex
    end: TileIndex


class Status(str, Enum):
    WHITE = "WHITE"
    BLACK = "BLACK"
    EMPTY = "EMPTY"


class Tile:
    x: conint(gt=0, lt=10)
    y: conint(gt=0, lt=10)
    status: Status


class Board:
    pass

