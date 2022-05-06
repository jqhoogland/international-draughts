from dataclasses import dataclass
from typing import Literal, Iterator

from checkers.models.position import row_of, col_of, floor_tile_index_of, TileIndex


class InvalidMoveError(ValueError):
    pass


@dataclass
class Move:
    """A move is essentially a vector pointing from a start tile to an end
    tile. It's slightly more complicated than "just a vector" because we're
    working with international draughts indexing.

    .. NOTE:: Actually, I lied: moves in different directions don't necessarily
       combine to form valid moves (though they might combine into valid series
       of captures) (closedness is a defining requirement of "vectors").

    """

    start: TileIndex
    end: TileIndex

    def unit(self) -> 'Move':
        """The equivalent of a unit vector for a move. Returns a move in the
        same direction with length-1 (i.e., one step)."""
        return self // len(self)

    def inverse(self) -> 'Move':
        return Move(self.end, self.start)

    def __post_init__(self):
        """To compute the "direction" of a move, we treat ``start`` as the origin
        and determine what quadrant ``end`` is in."""

        quadrant_unnormed = (row_of(self.end) - row_of(self.start),
                             col_of(self.end) - col_of(self.start))

        self.direction = (quadrant_unnormed[0] / (abs(quadrant_unnormed[0]) or 1),
                          quadrant_unnormed[1] / (abs(quadrant_unnormed[1]) or 1))

    def __add__(self, other: int) -> 'Move':
        """This is a bit of python magic that lets us override the standard
        ``+`` operation. In this case, we define adding an int to a move as
        extending the move in the direction of the line pointing from
        start to end.

        (This assumes that this a well-formed move.)
        """
        return Move(
            self.start,
            floor_tile_index_of(
                row_of(self.end) + self.direction[0] * other,
                col_of(self.end) + self.direction[1] * other,
                direction=(-self.direction[0], -self.direction[1])
            )
        )

    def __sub__(self, other: int) -> 'Move':
        """See ``__add__``. Subtraction is defined analogously but in the
        direction opposite the move."""
        return Move(
            self.start,
            floor_tile_index_of(
                row_of(self.end) - self.direction[0] * other,
                col_of(self.end) - self.direction[1] * other,
                direction=self.direction
            )
        )

    def __len__(self) -> int:
        """The number of steps (i.e., rows/cols) from ``start`` to ``end``."""
        row_len = abs(row_of(self.end) - row_of(self.start))
        col_len = abs(col_of(self.end) - col_of(self.start))

        if row_len != col_len and not (row_len == 0 or col_len == 0):
            raise InvalidMoveError("This move is off-diagonal. No cheating.")

        return max(row_len, col_len)

    def __floordiv__(self, other: int) -> 'Move':
        """Moves are vectorish. We should be able to multiply them.
        They're discrete, so we restrict division to floor division."""
        magnitude = len(self) // other

        return Move(
            self.start,
            floor_tile_index_of(
                row_of(self.start) + self.direction[0] * magnitude,
                col_of(self.start) + self.direction[1] * magnitude,
                direction=(-self.direction[0], -self.direction[1])
            )
        )

    def __mul__(self, other: int):
        """See __floordiv__. Included for completeness."""
        magnitude = len(self) * other

        return Move(
            self.start,
            floor_tile_index_of(
                row_of(self.start) + self.direction[0] * magnitude,
                col_of(self.start) + self.direction[1] * magnitude,
                direction=(-self.direction[0], -self.direction[1])
            )
        )

    def __iter__(self) -> Iterator[TileIndex]:
        """Returns an iterator over all of the tile indices encountered during this
        move along the diagonal, not including ``start`` but including ``end``)"""

        yield self.start

        step = self.unit()

        while row_of(step.end) != row_of(self.end) \
                and col_of(step.end) != col_of(self.end):
            yield step.end
            step = step + 1

        yield step.end


def capture_series_to_moves(idx: list[TileIndex]) -> list[Move]:
    return [Move(start, end) for start, end in zip(idx[:-1], idx[1:])]
