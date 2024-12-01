"""Classic Rock /  Scissors / Paper game.

A solo game of 'Rock Paper Scissors' against the computer.

The choices are cyclically arranged such that:
- Rock beats Scissors
- Scissors beats Paper
- Paper beats Rock

The game may be extended with more choices that follow the rules:
    1. Each item beats (n-1)//2 predecessors and is beaten by the
    other (n-1)//2 items (where 'n' is the number of items).
    2. There must be an odd number of choices.
    3. No choice may begin with 'Q' (reserved for 'Quit').
    4. All choices must begin with a unique letter.

If CHOICES is modified, it is highly recommended to test by running
the program with DEBUG enabled.

Example with more CHOICES options:

    ```python
    CHOICES = ('Rock', 'Batman', 'Paper', 'Lizard', 'Scissors')
    ```

"""

from dataclasses import dataclass
from functools import cache
import os
import random
import sys


CHOICES = ('Rock', 'Paper', 'Scissors')


@dataclass
class Scores:
    """Tally of score for games played."""

    player: int = 0
    robo: int = 0


def clear_screen() -> None:
    """Clear Terminal display."""
    if 'TERM' in os.environ:
        # Should work cross-platform for most terminals.
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        print('\n')  # In Thonny we settle for a new line.
        # Escape codes may work for other Terminal emulators.
        print("\n\033[H\033[J", end="")


@cache
def map_initial_to_name(choices: tuple[str]) -> dict[str, str]:
    """Map lowercase initial letter of name in choices, to name.

    Args:
        choices (tuple[str]): Game choices.

    Returns:
        dict[str: str]: key=first_letter, value=name.
    """
    return {name[0].lower(): name for name in choices}


@cache
def formatted_choices() -> str:
    """Return string of choices.

    Returns:
        str: The formatted string in the form '[R]ock, [P]aper, [S]cissors'.
    """
    return ', '.join([f"[{choice[0].upper()}]{choice[1:]}" for choice in CHOICES])


@cache
def formatted_input_choices() -> str:
    """Return string of input choice options.

    Although 'Q'/'q' is a valid input, it is for quitting rather than
    a game-play choice, so is not included.

    Returns:
        str: The formatted string in the form 'R', 'P', 'S'.
    """
    return ', '.join([f"'{name[0]}'" for name in CHOICES])


def player_choice() -> str:
    """Prompt and return human choice from CHOICES.

    Returns:
        str: The selected item from CHOICES.
    """
    while True:
        choice = input(f"{formatted_choices()}, or [Q] to quit: ")
        choice = choice.strip().lower()

        chosen = map_initial_to_name(CHOICES).get(choice)
        if chosen is not None:
            return chosen

        if 'q' == choice:
            quit_game()

        print(f"Invalid choice. Must be one of: {formatted_input_choices()}.")


def robo_choice() -> str:
    """Return computer choice.

    Returns:
        str: The randomly selected item from CHOICES.
    """
    return random.choice(CHOICES)


def display_result(game_score: Scores,
                   player: str = '',
                   robo: str = '',
                   result_str: str = '') -> None:
    """Display game result.

    Args:
        game_score (Scores): The current scores.
        player (str): The human player's choice.
        robo (str): The computer player's choice.
        result_str (str): The result announcement, such as 'WIN' or 'LOSE'.
    """
    clear_screen()

    if player != '':
        print(f"You = {player} : "
              f"Computer = {robo} : YOU {result_str}")
    print(f"Player: {game_score.player} | Computer: {game_score.robo}\n")


@cache
def beats(hand_choice: str) -> list[str]:
    """Return hand that is beaten by hand_choice.

    This assumes that each choice in CHOICES beats the item(s) that
    are cyclicly before the hand_choice, and is beaten by items after
    hand_choice. The result is cached as it only needs to be calculated
    once for each item in CHOICES.

    Args:
        hand_choice (str): The item from CHOICES to compare.

    Returns:
        str: The CHOICES items that beat 'hand_choice'.
    """
    idx = CHOICES.index(hand_choice)
    number_of_beaten_items = (len(CHOICES) - 1) // 2
    beaten = [CHOICES[idx - i - 1] for i in range(number_of_beaten_items)]

    return beaten


def is_player_winner(player: str, robo: str) -> bool | None:
    """Return True, False or None to indicate result.

    Args:
        player (str): The human player's choice.
        robo (str): The computer player's choice.

    Returns:
        bool | None:
            - True when player wins.
            - False when player loses.
            - None when a draw.

    Note:
        Comparison is performed on long names, rather than
        the user-entered abbreviations.
    """
    if player == robo:
        return None

    return robo in beats(player)


def quit_game():
    """Quit application."""
    print("Bye")
    sys.exit(0)


def main():
    """Game loop."""
    scores = Scores()
    display_result(scores)

    while True:
        player_hand = player_choice()
        robo_hand = robo_choice()

        result = is_player_winner(player_hand, robo_hand)

        if result is None:
            display_result(scores, player_hand, robo_hand, "DRAW")

        elif result:
            scores.player += 1
            display_result(scores, player_hand, robo_hand, "WIN")

        else:
            scores.robo += 1
            display_result(scores, player_hand, robo_hand, "LOSE")


if __name__ == '__main__':
    main()
