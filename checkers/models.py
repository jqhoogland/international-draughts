from dataclasses import dataclass
from pydantic import pydantic, conint
from enum import Enum


class Status(str, Enum):
    WHITE = "WHITE"
    BLACK = "BLACK"
    EMPTY = "EMPTY"


@pydantic
class Tile:
    x: conint(gt=0, lt=10)
    y: conint(gt=0, lt=10)
    status: Status


@pydantic
class Board:


