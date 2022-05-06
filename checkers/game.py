import re
from dataclasses import dataclass
from typing import Union, Optional

from checkers.logic.max_capture import validate_max_capture
from checkers.logic.rules import validate_step, validate_captures
from checkers.models import Move, Board, capture_series_to_moves, Piece
from checkers.models.board import InvalidMoveError


def parse_cmd(cmd) -> Union[Move, list[Move]]:
    if match := re.search(r"(\d{1,2})\-(\d{1,2})", cmd):
        start, end = match.group(1), match.group(2)
        return Move(int(start), int(end))

    elif idxs := list(map(int, cmd.split("x"))):
        return capture_series_to_moves(idxs)

    raise InvalidMoveError(f"Couldn't parse the given move '{cmd}'")


def default_board() -> Board:
    return Board(list(range(31, 51)), list(range(1, 21)))


@dataclass(init=False)
class Game:
    """A proxy for ``Board`` that parses (user-inputted) string commands into
    moves and validates them before updating the board."""
    board: Board

    def play(self, cmd: str):
        if cmd.strip() == "exit":
            raise StopIteration

        move = parse_cmd(cmd)

        if isinstance(move, Move):
            piece = self._play_step(move)
        else:
            piece = self._play_captures(move)

        if piece.has_reached_end:
            self.board.replace(piece.coronate())

    def play_turn(self, p1_move: str, p2_move: str):
        """Convenience method that plays two moves (a single turn) at once."""
        self.play(p1_move)
        self.play(p2_move)

    def _play_step(self, move: Move) -> Piece:
        validate_step(self.board, move)  # -> InvalidMoveError
        self.board = self.board.apply_step(move)
        return self.board[move.end]

    def _play_captures(self, moves: list[Move]) -> Piece:
        validate_captures(self.board, moves)  # -> InvalidMoveError
        validate_max_capture(self.board, moves)
        self.board = self.board.apply_captures(moves)
        return self.board[moves[-1].end]

    def __init__(self, board: Optional[Board] = None):
        self.board = board or default_board()
