"""Classic Rock / Scissors / Paper Game.

A solo game of 'Rock Paper Scissors' against the computer.

Rules:
The choices are cyclically arranged such that:
    - Rock beats Scissors
    - Scissors beats Paper
    - Paper beats Rock

The game may be extended with more choices that follow the rules:
    1. Each item beats (n-1)//2 predecessors and is beaten by the other
       (n-1)//2 items (where 'n' is the number of items).
    2. There must be an odd number of choices.
    3. No choice may begin with the `QUIT_KEY` character.
    4. All choices must begin with a unique letter.

If `DEFAULT_CHOICES` is modified, it is highly recommended to validate the
choices by running the pytests.

Examples:
To add more choice options, use a tuple like this::

    ('Rock', 'Batman', 'Paper', 'Lizard', 'Scissors')

The rules for extended choices would be:

    - Rock beats: Scissors and Lizard
    - Batman beats: Rock and Scissors
    - Paper beats: Batman and Rock
    - Lizard beats: Paper and Batman
    - Scissors beats: Lizard and Paper

Case-Insensitive Input Handling:
Although lowercase normalization is more common, user input is normalized
to uppercase to match the displayed menu options. For example: 'R', 'P', 'S'.
"""
import logging
from collections import Counter
from dataclasses import dataclass
import os
import random
import sys


logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])


DEFAULT_CHOICE_NAMES = ('Rock', 'Paper', 'Scissors')
QUIT_KEY = 'Q'  # Reserved for quitting the program.

GestureNames = tuple[str, ...]


@dataclass
class Scores:
    """Tally of score for games played."""

    player: int = 0
    robo: int = 0


class GameConfig:
    """Configuration object.

    Game choices and derived constants are encapsulated in the GameConfig object.
    """

    def __init__(self, choice_names: GestureNames) -> None:
        """Initialize game configuration object."""
        self._choices: GestureNames = self.validate_choices(choice_names)
        # Derived properties.
        self._choice_map: dict[str, str] = self._map_initial_to_name()
        self._choices_str: str = self._format_choices()
        self._user_input_choices: str = self._formatted_input_choices()
        self._cyclic_hierarchy_map: dict[str, list[str]] = self._map_cyclic_hierarchy()

    @staticmethod
    def validate_choices(choices: GestureNames) -> GestureNames:
        """There must be an odd number of at least 3 choices.

        The number of choices must be odd so that each choice beats the
        same number of choices as it is beaten by. Three choices is the
        minimum number required to ensure that each choice can win and lose.
        Each choice must start with a unique letter (case-insensitive) as
        choices are made by selecting the first letter.

        Args:
            choices (GestureNames): The tuple of hands to choose from.

        Raises:
            TypeError: The choices are not tuple[str, ...].
            ValueError: The choices are invalid.

        Returns:
            GestureNames: The validated choices.
        """
        if not isinstance(choices, tuple):
            raise TypeError("Tuple required. "
                            f"Received {type(choices)}")

        if len(choices) < 3:
            raise ValueError("3 or more choices required. "
                             f"Received {len(choices)}")

        if len(choices) % 2 == 0:
            raise ValueError("Number of choices must be odd.")

        # Check for duplicates.
        if len(choices) != len(set(choices)):
            count = Counter(choices)
            duplicates = [choice for choice, num in count.items() if num > 1]
            raise ValueError(f"Duplicate choice: {duplicates}")

        # Check each choice is a string beginning with a unique letter.
        # First letter check is case-insensitive as they are represented uppercase.
        first_letters = set()
        for choice in choices:
            if not isinstance(choice, str):
                raise TypeError("Each choice must be a string. "
                                f"Received {type(choice)}")
            if choice[0].upper() in first_letters:
                raise ValueError("Each choice must begin with a unique letter. "
                                 f"Duplicate found: '{choice[0]}'.")
            first_letters.add(choice[0].upper())

        return choices

    @property
    def choices(self) -> GestureNames:
        """Tuple of game choices.

        By default, this returns the strings 'Rock', 'Paper', 'Scissors' from
        DEFAULT_CHOICE_NAMES. If you wish to modify the available choices, ensure
        that you validate them by running the `test_default_choices.py` pytest.

        Returns:
            GestureNames: The game choice names.
        """
        return self._choices

    @property
    def choice_map(self) -> dict[str, str]:
        """Return a dict of initial letters to choice names.

        Returns:
            dict: The map, {initial_letter: full_name, ...}.
        """
        return self._choice_map

    @property
    def reverse_choice_map(self) -> dict[str, str]:
        """Return a map of choice names to initial letters.

        Returns:
            dict: The map {full_name: initial_letter, ...}
        """
        assert self._choice_map is not None
        return {name: key for key, name in self._choice_map.items()}

    @property
    def formatted_choices(self) -> str:
        """Return formatted string of choices.

        Returns:
            str: The formatted string in the form '[R]ock, [P]aper, [S]cissors'.
        """
        return self._choices_str

    @property
    def user_input_choices(self) -> str:
        """Return string of input choice options.

        Although QUIT_KEY (Default 'Q'/'q') is a valid input, it is reserved
        for quitting rather than a game-play choice, so is not included.

        Returns:
            str: The formatted string in the form "'R', 'P', 'S'".
        """
        return self._user_input_choices

    @property
    def is_beaten_by(self) -> dict[str, list[str]]:
        """A dictionary defines which hands are beaten by each choice.

        Dictionary in the form: {winner: list[losers], ...}
        """
        return self._cyclic_hierarchy_map

    def _map_initial_to_name(self) -> dict[str, str]:
        """Map uppercase initial letter of name in choices, to name."""
        return {name[0].upper(): name for name in self.choices}

    def _format_choices(self) -> str:
        """Return formatted string of choices."""
        return ', '.join([f"[{choice[0].upper()}]{choice[1:]}"
                          for choice in self.choices])

    def _formatted_input_choices(self) -> str:
        """Return string of input choice options."""
        return ', '.join([f"'{name[0].upper()}'" for name in self.choices])

    def _map_cyclic_hierarchy(self) -> dict[str, list[str]]:
        """Return dict mapping each choice to a list of choices that it beats."""
        number_of_beaten = (len(self._choices) - 1) // 2
        hierarchy_map = {}
        for idx, choice in enumerate(self.choices):
            beaten = [self._choices[idx - j - 1] for j in range(number_of_beaten)]
            hierarchy_map[choice] = beaten
        return hierarchy_map


class Hands:
    """Hands objects represent the hand gestures made by players of this game.

    Each "hand" object  has a:

    - name (such as "Rock")
    - menu name ("[R]ock")
    - user choice name ("R")
    - "is_beaten_by" property (a list of other "hands").
    """

    def __init__(self, config: GameConfig, hand_choice: str) -> None:
        """Instantiate a hand from hand_choice.

        Args:
            config (GameConfig): Configuration object of choices for current game.
            hand_choice (str): The kind of hand required. This may be the hand name
                (eg "Rock") or the hand choice key (eg "R").
        """
        self.config = config
        self.choice_key = None
        self.name = None
        self.is_beaten_by = config.is_beaten_by
        self.validate_choice(hand_choice)

    def validate_choice(self, choice):
        """Validate hand_choice and assign self.name and self.choice_key.

        Args:
            choice (str): The user's  choice. This may be the name or choice_key.

        Raises:
            ValueError: If the user's choice is not valid.
        """
        if choice in self.config.user_input_choices:
            self.choice_key = choice
            self.name = self.config.choice_map[choice]
        elif choice in self.config.choices:
            self.name = choice
            self.choice_key = self.config.reverse_choice_map[choice]
        else:
            raise ValueError(f"Invalid choice '{choice}'")

    def beats(self, other_hand) -> bool:
        """Return True if this hand beats other_hand.

        Args:
            other_hand: The hand to beat.

        Returns:
            bool: True if this hand wins, else False
        """
        return other_hand.name in other_hand.is_beaten_by[self.name]

    def __eq__(self, other):
        """Hands considered equal if name the same."""
        if isinstance(other, Hands):
            return self.name == other.name
        return False


def clear_screen() -> None:
    """Clear Terminal display."""
    if 'TERM' in os.environ:
        # Should work cross-platform for most terminals.
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        print('\n')  # In Thonny we settle for a new line.
        # Escape codes may work for other Terminal emulators.
        print("\n\033[H\033[J", end="")


def player_choice(config: GameConfig) -> Hands:
    """Prompt and return human's hand gesture object.

    Returns:
        Hands: The selected Hand() object.
    """
    while True:
        choice = input(f"{config.formatted_choices}, or [{QUIT_KEY}] to quit: ")
        choice = choice.strip().upper()

        if QUIT_KEY == choice:
            quit_game()

        try:
            return Hands(config, choice)
        except ValueError:
            print(f"Invalid choice. Must be one of: {config.user_input_choices}.")


def robo_choice(config: GameConfig) -> Hands:
    """Return a randomly selected hand gesture object.

    Args:
        config (GameConfig): The game configuration.

    Returns:
        Hands: The randomly selected hand object.
    """
    return Hands(config, random.choice(config.choices))


def display_result(game_score: Scores,
                   player: str = '',
                   robo: str = '',
                   result_str: str = '') -> None:
    """Display game result.

    Args:
        game_score (Scores): The current scores.
        player (str): The human player's hand name.
        robo (str): The computer player's hand name.
        result_str (str): The result announcement, of 'WIN', 'LOSE' or 'DRAW'.
    """
    clear_screen()

    if player != '':
        print(f"You = {player} : "
              f"Computer = {robo} : YOU {result_str}")
    print(f"Player: {game_score.player} | Computer: {game_score.robo}\n")


def quit_game():
    """Exit the game and terminate the program."""
    print("Bye")
    sys.exit(0)


def main(config: GameConfig):
    """Game loop."""
    scores = Scores()
    display_result(scores)

    while True:
        player_hand: Hands = player_choice(config)
        robo_hand: Hands = robo_choice(config)

        if player_hand == robo_hand:
            display_result(scores, player_hand.name, robo_hand.name, "DRAW")

        elif player_hand.beats(robo_hand):
            scores.player += 1
            display_result(scores, player_hand.name, robo_hand.name, "WIN")

        else:
            scores.robo += 1
            display_result(scores, player_hand.name, robo_hand.name, "LOSE")


if __name__ == '__main__':
    default_config = GameConfig(DEFAULT_CHOICE_NAMES)
    main(default_config)
