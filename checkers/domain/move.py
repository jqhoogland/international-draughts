from typing import NamedTuple, Literal, Iterator

from checkers.domain.board import TileIndex
from checkers.utils import row_of, col_of, tile_index_of


class Move(NamedTuple):
    start: TileIndex
    end: TileIndex

    @property
    def direction(self) -> tuple[Literal[1, -1], Literal[1, -1]]:
        """To compute the "direction" of a move, we treat ``start`` as the origin
        and determine what quadrant ``end`` is in."""

        quadrant_unnormed = (row_of(self.end) - row_of(self.start),
                             col_of(self.end) - col_of(self.start))
        return (quadrant_unnormed[0] / abs(quadrant_unnormed[0]),
                quadrant_unnormed[1] / abs(quadrant_unnormed[1]))

    def __add__(self, other: int) -> 'Move':
        """This is a bit of python magic that lets us override the standard
        ``+`` operation. In this case, we define adding an int to a move as
        extending the move in the direction of the diagonal pointing from
        start to end.

        (This assumes that this a well-formed move.)
        """

        direction = self.direction

        return Move(
            self.start,
            tile_index_of(
                row_of(self.end) + direction[0] * other,
                col_of(self.end) + direction[1] * other
            )
        )

    def __sub__(self, other: int) -> 'Move':
        """See ``__add__``. Subtraction is defined analogously but in the
        direction opposite the move."""

        direction = self.direction

        return Move(
            self.start,
            tile_index_of(
                row_of(self.end) - direction[0] * other,
                col_of(self.end) - direction[1] * other
            )
        )

    def __iter__(self) -> Iterator[TileIndex]:
        """Returns an iterator over all of the tile indices encountered during this
        move, not including ``start`` but including ``end``. """

        direction = self.direction

        step = Move(
            self.start,
            tile_index_of(
                row_of(self.end) + direction[0],
                col_of(self.end) + direction[1]
            )
        )

        yield step.end

        while row_of(step.end) <= row_of(self.end) and col_of(step.end) <= col_of(self.end):
            step = step + 1
            yield step.end


def capture_series_to_moves(idx: list[TileIndex]) -> list[Move]:
    return [Move(start, end) for start, end in zip(idx[:-1], idx[1:])]