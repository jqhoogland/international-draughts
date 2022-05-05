from typing import Literal

PLAYER_ONE = True
PLAYER_TWO = False
Player = Literal[PLAYER_ONE, PLAYER_TWO]  # I.e. bool (just a tad more explicit).