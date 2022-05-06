from checkers.io.sample_match import sample_game_cmd_generator


def test_sample_game():
    sample_game = sample_game_cmd_generator()

    assert next(sample_game) == (1, ["32-28", "19-23"])
    assert next(sample_game) == (2, ["28x19", "14x23"])
