from typing import Literal

PLAYER_ONE = True
PLAYER_TWO = False
Player = Literal[PLAYER_ONE, PLAYER_TWO]

# In retrospect, using a bool actually isn't great here.
# It'd be better to use an enum with a __not__ or __isub__ implemented for inversion.
