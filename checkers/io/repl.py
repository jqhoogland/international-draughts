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

from checkers.models.game import Game
from checkers.models.move import InvalidMoveError
from checkers.utils.draw import draw_centered_board_with_indices, draw_tile_indices
from checkers.utils.stringx import HR, center_text, wrap_text


def std_input_cmd_generator(get_prompt=lambda i: None, invalid_move_error_handler=lambda e: None):
    turn_idx = 1

    while True:
        try:
            yield turn_idx, input(get_prompt(turn_idx))
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

{center_text(" International Draughts ", char="*")}
{center_text(" Author: Jesse Hoogland ", char="*")}
    
{center_text(wrap_text("Source: https://github.com/jqhoogland/international-draughts", width=60))}

{center_text(wrap_text(RULES, width=60))}    

{center_text(draw_tile_indices())}

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

    for turn_idx, move in std_input_cmd_generator(
            get_prompt=get_prompt,
            invalid_move_error_handler=handle_invalid_move
    ):
        game.play(move)
        print(draw_centered_board_with_indices(game.board))

    print(draw_centered_board_with_indices(game.board))
    print(get_footer())


if __name__ == "__main__":
    main()
