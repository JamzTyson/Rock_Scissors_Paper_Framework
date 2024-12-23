"""Test data for pytests."""


def valid_data():
    """Validate test configurations and expected results.

    For each HandNames tuple, we have a dict of expected valuesL
        - 'valid_HandNames' -> (tuple[str]): The tuple of GameOption names.
        - 'choice_keys' -> (list[str]): The choice keys.
    """
    return [
        # Default test.
        (
            ("Rock", "Paper", "Scissors"),
            {
                "valid_HandNames": ("Rock", "Paper", "Scissors"),
                "choice_keys": ["R", "P", "S"],
            },
        ),
        # Mixed case names are allowed.
        (
            ("aaA", "BBB", "Ccc", "dDD", "eee"),
            {
                "valid_HandNames": ("aaA", "BBB", "Ccc", "dDD", "eee"),
                "choice_keys": ["A", "B", "C", "D", "E"],
            },
        ),
        # Numeric characters are allowed.
        (
            ("123", "456", "789"),
            {"valid_HandNames": ("123", "456", "789"),
             "choice_keys": ["1", "4", "7"]},
        ),
        # Names with spaces or special characters are allowed
        # so long as not leading whitespace.
        (
            ("Hello World", "a b c", "&£$*%-_"),
            {
                "valid_HandNames": ("Hello World", "a b c", "&£$*%-_"),
                "choice_keys": ["H", "A", "&"],
            },
        ),
        # Single character names are allowed.
        (
            ("a", "b", "c"),
            {
                "valid_HandNames": ("a", "b", "c"),
                "choice_keys": ["A", "B", "C"],
            },
        ),
        # Leading / trailing whitespace is allowed, but is stripped from names
        (
            ("a  ", "b", "c   "),
            {
                "valid_HandNames": ("a", "b", "c"),
                "choice_keys": ["A", "B", "C"],
            },
        ),
        # Leading tab (whitespace) is allowed but stripped.
        (
            ("\ta", "b", "c"),
            {
                "valid_HandNames": ("a", "b", "c"),
                "choice_keys": ["A", "B", "C"],
            },
        ),
    ]


def invalid_data():
    """Invalid configuration data, and expected exceptions.

    Used to test that GameConfig functions correctly when passed
    an invalid argument.

    choices, expected_exception.
    """
    return [
        # Must be at least 3 choices.
        ((), ValueError),
        (("Rock",), ValueError),
        (("Rock", "Paper"), ValueError),

        # Choices must be strings.
        (("rock", "scissors", 42), TypeError),

        # Must be an odd number of choices.
        (("Rock", "Paper", "Scissors", "Lizard"), ValueError),

        # First character must be unique (case-insensitive).
        (("rock", "Rock", "Paper"), ValueError),
        (("Rock", "Paper", "Scissors", "Lizard", "Superman"), ValueError),

        # Choice cannot be an empty string.
        (("Rock", "", "Paper"), ValueError),
    ]
