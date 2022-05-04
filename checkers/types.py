from pydantic import conint

TileIndex = conint(ge=1, le=50)
RowIndex = conint(ge=0, lt=10)
ColIndex = conint(ge=0, lt=10)
