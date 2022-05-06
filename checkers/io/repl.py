"""
--------------------------------------------------------------------------------

**************************** International Draughts ****************************
**************************** Author: Jesse Hoogland ****************************

          Source: https://github.com/jqhoogland/international-draughts

          Provide your moves using international draughts standard
          notation:

          - Normal steps are indicated with a hyphen (e.g., `32-28`).
          - Captures are indicated with an `x` (e.g, `39x28x17`).

          For reference, tiles are indexed as follows:

                        |  |01|  |02|  |03|  |04|  |05|
                        |06|  |07|  |08|  |09|  |10|  |
                        |  |11|  |12|  |13|  |14|  |15|
                        |16|  |17|  |18|  |19|  |20|  |
                        |  |21|  |22|  |23|  |24|  |25|
                        |26|  |27|  |28|  |29|  |30|  |
                        |  |31|  |32|  |33|  |34|  |35|
                        |36|  |37|  |38|  |39|  |40|  |
                        |  |41|  |42|  |43|  |44|  |45|
                        |46|  |47|  |48|  |49|  |50|  |


--------------------------------------------------------------------------------
"""

from checkers.game import Game
from checkers.models.move import InvalidMoveError
from checkers.utils.draw import draw_centered_board_with_indices, draw_tile_indices
from checkers.utils.stringx import HR, center_multiline, wrap_text


def std_input_cmd_generator(get_prompt=lambda i: None, invalid_move_error_handler=lambda e: None):
    turn_idx = 1

    while True:
        try:
            yield turn_idx // 2, input(get_prompt(turn_idx))
            turn_idx += 1

        except InvalidMoveError as e:
            invalid_move_error_handler(e)


RULES = """Provide your moves using international draughts standard notation:

- Normal steps are indicated with a hyphen (e.g., `32-28`).
- Captures are indicated with an `x` (e.g, `39x28x17`).

For reference, tiles are indexed as follows:"""


def get_intro() -> str:
    return f"""

{HR}

{center_multiline(" International Draughts ", char="*")}
{center_multiline(" Author: Jesse Hoogland ", char="*")}
    
{center_multiline(wrap_text("Source: https://github.com/jqhoogland/international-draughts", width=60))}

{center_multiline(wrap_text(RULES, width=60))}    

{center_multiline(draw_tile_indices())}

{HR}

    """


def get_footer() -> str:
    return "\nThanks for playing!"


def main():
    game = Game()

    print(get_intro())
    print(draw_centered_board_with_indices(game.board))

    def get_prompt(turn_idx: 'TurnIndex') -> str:
        return f"> {str(turn_idx).zfill(2)} (P{1 + (turn_idx // 2)}). "

    def handle_invalid_move(e: InvalidMoveError):
        print(f"{e} Please try again.")

    try:
        for turn_idx, move in std_input_cmd_generator(
                get_prompt=get_prompt,
                invalid_move_error_handler=handle_invalid_move
        ):
            game.play(move)

            print("\n")
            print(draw_centered_board_with_indices(game.board))
            print("\n")

    except StopIteration:
        pass

    print(draw_centered_board_with_indices(game.board))
    print(get_footer())


if __name__ == "__main__":
    main()

# THe same game as in sample_match (but structured to copy-paste into the shell)
SAMPLE_GAME = """32-28
19-23
28x19
14x23
37-32
10-14
41-37
05-10
46-41
14-19
32-28
23x32
37x28
09-14
38-32
16-21
31-26
18-22
43-38
12-18
49-43
07-12
36-31
11-16
31-27
22x31
26x37
21-27
32x21
17x26
34-30
19-24
30x19
14x23x32
37x28
20-24
40-34
10-14
45-40
14-20
34-30
03-09
30x19
13x24
40-34
09-13
44-40
16-21
34-30
06-11
30x19
13x24
39-34
08-13
34-30
02-08
30x19
13x24
40-34
04-09
43-39
09-13
48-43
11-17
41-37
01-07
34-30
20-25
30x19
13x24
39-34
08-13
43-39
07-11
50-44
13-19
38-32
18-23
28-22
17x28
33x22
12-17
42-38
17x28
38-33
15-20
33x22
24-29
22-17
29x40x49
17x06
49x27
06-01
27-31
01x29x15
31x48x34
35-30
exit
"""
        