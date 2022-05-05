
from checkers.draw import draw_tile_indices, draw_board_with_indices
from checkers.io.sample import sample_game_cmd_generator
from checkers.setup import default_board


def std_input_cmd_generator():
    turn_idx = 1
    while True:
        print(f"> {str(turn_idx).zfill(2)}.")
        yield turn_idx, input()
        turn_idx += 1


def main():
    """Notation obeys standard international checkers notation:
    - Normal steps are indicated by a hyphen (e.g., `32-28`)
    - Captures are indicated by an `x` (e.g., `39x28x17`)

    """

    board = default_board()

    cmd_generator = std_input_cmd_generator()

    try:
        while True:
            print("\n\n" + "-" * 80 + "\n\n")
            print(draw_board_with_indices(board))
            print("\n")
            turn_idx, cmd = next(cmd_generator)

            if cmd == "\\i":  # Show indexes
                print("The tiles are indexed from top-left to bottom-right, as follows:")
                print(draw_tile_indices())
            elif cmd == "\\s":  # Show sample
                print("Showing a sample game...")
                cmd_generator = sample_game_cmd_generator()
            else:
                board.apply(cmd)

    except StopIteration:
        print("\nThanks for playing!")


if __name__ == "__main__":
    main()