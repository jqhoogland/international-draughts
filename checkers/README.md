# (International) Checkers

> An implementation in Python.

---

## Rules

### Starting position

- **The Board**: The game is played on a 10 x 10 "checkered" grid (starting with a dark tile on the bottom left).
- **Piece Placement**: Board are allowed only on dark tiles. Players start with 20 of their pieces filling the dark
  tiles in their four closest rows.

### Movement

- Ordinary pieces move one square diagonally forward.
- Ordinary pieces can capture by jumping over an enemy piece into an empty tile two squares forward or backwards (along
  the diagonal).
- A single piece can make successive captures (but capture pieces are not removed until the end of the turn and can only
  be jumped once).
- A player must obey "maximum capture" and choose the move that captures the most possible pieces.

### Kings

- A piece becomes a king if it *ends its turn* on the far edge opposing the player.
- A king can take multiple steps in any direction.
- A king can jump over and capture an enemy piece any distance away and choose where to stop after.

### Endgame

- A player loses if they cannot make any valid moves.
- A game draws if:
    - a position repeats itself three times, or
    - the players end up with only (equal numbers of kings), or
    - during 25 moves, there are only king moves without normal piece moves or captures.
    - after 16 moves if there are only three kings, two kings and a piece, or a king and two pieces against a king
    - a player proposes a draw (and there have been at least 40 moves).

---

## Notation

Dark squares are numbered from 1 to 50 starting with the leftmost square in the top row, moving left-to-right, then
top-down.
