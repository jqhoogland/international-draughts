from checkers.io.sample import sample_game_cmd_generator


def test_sample_game():
    sample_game = sample_game_cmd_generator()

    assert next(sample_game) == (1, "32-28")
    assert next(sample_game) == (1, "19-23")
    assert next(sample_game) == (2, "28x19")
    assert next(sample_game) == (2, "14x23")
    assert next(sample_game) == (3, "37-32")