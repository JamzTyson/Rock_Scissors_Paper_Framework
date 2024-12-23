"""Tests to validate DEFAULT_CHOICES tuple."""
import string
from collections import defaultdict

from ..rsp import DEFAULT_CHOICE_NAMES, QUIT_KEY


def test_is_tuple():
    """DEFAULT_CHOICES should be a tuple."""
    assert isinstance(DEFAULT_CHOICE_NAMES, tuple)


def test_choice_strings():
    """Each item in `DEFAULT_CHOICES` must be a printable string."""
    for choice in DEFAULT_CHOICE_NAMES:
        assert isinstance(choice, str), f"Choice '{choice}' is not a string."
        message = f"Choice '{choice}' contains non-printable characters."
        assert all(c in string.printable for c in choice), message


def test_length():
    """Number of choices must be greater than 1."""
    assert len(DEFAULT_CHOICE_NAMES) > 1


def test_odd_number():
    """Number of choices must be odd."""
    assert len(DEFAULT_CHOICE_NAMES) % 2 == 1


def test_not_start_with_q():
    """No choice can begin with QUIT_KEY (default: 'Q')."""
    for choice in DEFAULT_CHOICE_NAMES:
        assert choice[0].upper() != QUIT_KEY, f"Bad option: {choice}"


def test_not_start_with_space():
    """No choice can begin with a space."""
    for choice in DEFAULT_CHOICE_NAMES:
        assert not choice[0] == ' ', f"Bad option: {choice}"


def test_no_empty_names():
    """No choice can be an empty string."""
    for choice in DEFAULT_CHOICE_NAMES:
        assert choice != '', "Bad option: Empty string"
        assert choice != '', "Bad option: Empty string"


def test_unique_first_letter():
    """Each choice must have a unique first letter (case-insensitive)."""
    first_letters = defaultdict(list)
    for choice in DEFAULT_CHOICE_NAMES:
        first_letters[choice[0].upper()].append(choice)
    duplicates = {k: v for k, v in first_letters.items() if len(v) > 1}
    assert len(duplicates) == 0, f"Duplicate first letters found: {duplicates}"
