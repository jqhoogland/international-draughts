import re
from dataclasses import dataclass
from typing import Union

from checkers.domain import Move, Board, capture_series_to_moves, Piece
from checkers.domain.board import InvalidMoveFormat
from checkers.setup import default_board
from checkers.validation import validate_step, validate_captures


def parse_cmd(cmd) -> Union[Move, list[Move]]:
    if match := re.search(r"(\d{1,2})\-(\d{1,2})", cmd):
        start, end = match.group(1), match.group(2)
        return Move(int(start), int(end))

    elif idxs := list(map(int, cmd.split("x"))):
        return capture_series_to_moves(idxs)

    raise InvalidMoveFormat(f"Couldn't parse the given move '{cmd}'")


@dataclass(init=False)
class Game:
    board: Board

    def _play_step(self, move: Move) -> Piece:
        validate_step(self.board, move)
        self.board = self.board.apply_step(move)
        return self.board[move.end]

    def _play_captures(self, moves: list[Move]) -> Piece:
        validate_captures(self.board, moves)
        self.board = self.board.apply_captures(moves)
        return self.board[moves[-1].end]

    def play(self, cmd: str):
        move = parse_cmd(cmd)

        if isinstance(move, Move):
            piece = self._play_step(move)
        else:
            piece = self._play_captures(move)

        if piece.has_reached_end:
            self.board.replace(piece.coronate())

    def __init__(self):
        self.board = default_board()

