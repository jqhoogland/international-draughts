from typing import TypeVar

from pydantic import conint, conlist

T = TypeVar("T")

TileIndex = conint(ge=1, le=50)
RowIndex = conint(ge=0, lt=10)
ColIndex = conint(ge=0, lt=10)


def tilelist(item_type: T):
    return conlist(T, min_items=50, max_items=50)
