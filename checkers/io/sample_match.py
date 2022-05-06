"""
--------------------------------------------------------------------------------


                                  Sample Match


**************************** Milsjin,W. - Salomé,G. ****************************
**************************** Confederation Cup 2000 ****************************


          Source: https://drive.google.com/file/d/0B2XFf6MWShkeYjU5NzQ
          1YTQtNGIwMS00ZjRiLWJlNmUtZDQ0MDNiNDE3MDE0/view?hl=en&resourc


--------------------------------------------------------------------------------
"""
import time

from checkers.models.game import Game
from checkers.utils.draw import draw_centered_board_with_indices
from checkers.utils.stringx import wrap_text, center_multiline, HR

SAMPLE_GAME = """01.32-28 19-23
02.28x19 14x23
03.37-32 10-14
04.41-37 05-10
05.46-41 14-19
06.32-28 23x32
07.37x28 09-14
08.38-32 16-21
09.31-26 18-22
10.43-38 12-18
11.49-43 07-12
12.36-31 11-16
13.31-27 22x31
14.26x37 21-27
15.32x21 17x26
16.34-30 19-24
17.30x19 14x23x32
18.37x28 20-24
19.40-34 10-14
20.45-40 14-20
21.34-30 03-09
22.30x19 13x24
23.40-34 09-13
24.44-40 16-21
25.34-30 06-11
26.30x19 13x24
27.39-34 08-13
28.34-30 02-08
29.30x19 13x24
30.40-34 04-09
31.43-39 09-13
32.48-43 11-17
33.41-37 01-07
34.34-30 20-25
35.30x19 13x24
36.39-34 08-13
37.43-39 07-11
38.50-44 13-19
39.38-32 18-23
40.28-22 17x28
41.33x22 12-17
42.42-38 17x28
43.38-33 15-20
44.33x22 24-29
45.22-17 29x40x49
46.17x06 49x27
47.06-01 27-31
48.01x29x15 31x48x34
49.35-30 exit"""

TurnIndex = int
MoveStr = str


def sample_game_cmd_generator() -> tuple[TurnIndex, tuple[MoveStr, MoveStr]]:
    """
    Expects a text string of turns separated by ``\n``, where each turn is in the
    format: ``<turn-#>.<move-player-1> <move-player-2>`

    This is a generator over successive turns (alternating between players)
    """

    for turn in SAMPLE_GAME.split("\n"):
        turn_idx, moves = turn.split(".")
        yield int(turn_idx), moves.split(" ")


def get_intro() -> str:
    return f"""
    
    {HR}
    
    {center_multiline("Sample Match")}
    
    {center_multiline(" Milsjin,W. - Salomé,G. ", char="*")}
    {center_multiline(" Confederation Cup 2000 ", char="*")}
    {center_multiline(wrap_text("Source: https://drive.google.com/file/d/0B2XF"
                           "f6MWShkeYjU5NzQ1YTQtNGIwMS00ZjRiLWJlNmUtZDQ0M"
                           "DNiNDE3MDE0/view?hl=en&resourcekey=0-YKq77m5g"
                           "8Nc1VcLmMpQzcg", width=60))
    }
    
    {HR}
    
    """


def get_footer():
    return f"""
    
    {HR}
    
    """


def draw_move(turn_idx: TurnIndex, p1_move: MoveStr, p2_move: MoveStr) -> str:
    return f"> {str(turn_idx).zfill(2)}.{p1_move} {p2_move}"


def main():
    game = Game()

    print(get_intro())
    time.sleep(2)

    for turn_idx, (p1_move, p2_move) in sample_game_cmd_generator():
        print(draw_centered_board_with_indices(game.board))
        print(draw_move(turn_idx, p1_move, p2_move))
        game.play_turn(p1_move, p2_move)

    print(draw_centered_board_with_indices(game.board))
    print(get_footer())


if __name__ == "__main__":
    main()
