from pydantic import conint, conlist

TileIndex = conint(ge=1, le=50)
RowIndex = conint(ge=0, lt=10)
ColIndex = conint(ge=0, lt=10)


def tilelist(item_type):
    return conlist(item_type, min_items=50, max_items=50)
