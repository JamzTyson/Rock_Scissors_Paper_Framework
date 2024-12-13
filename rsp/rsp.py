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
To add more choice _options, use a tuple like this::

    ('Rock', 'Batman', 'Paper', 'Lizard', 'Scissors')

The rules for extended choices would be:

    - Rock beats: Scissors and Lizard
    - Batman beats: Rock and Scissors
    - Paper beats: Batman and Rock
    - Lizard beats: Paper and Batman
    - Scissors beats: Lizard and Paper

Case-Insensitive Input Handling:
Although lowercase normalization is more common, user input is normalized
to uppercase to match the displayed menu _options. For example: 'R', 'P', 'S'.
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

HandNames = tuple[str, ...]


@dataclass
class Scores:
    """Tally of score for games played."""

    player: int = 0
    robo: int = 0


class GameOptions:
    """Configuration object.

    Game choices and derived constants are encapsulated in the GameOptions object.
    """

    def __init__(self, choice_names: HandNames) -> None:
        """Initialize game configuration object."""
        self._hand_names: HandNames = self.validate_choices(choice_names)
        # Derived properties.
        self._choice_keys: list[str] = self.generate_choice_keys()
        self._choice_map: dict[str, str] = self._map_initial_to_name()
        self._cyclic_hierarchy_map: dict[str, list[str]] = self._map_cyclic_hierarchy()

    @staticmethod
    def validate_choices(choices: HandNames) -> HandNames:
        """There must be an odd number of at least 3 choices.

        The number of choices must be odd so that each choice beats the
        same number of choices as it is beaten by. Three choices is the
        minimum number required to ensure that each choice can win and lose.
        Each choice must start with a unique letter (case-insensitive) as
        choices are made by selecting the first letter.

        Args:
            choices (HandNames): The tuple of _hands to choose from.

        Raises:
            TypeError: The choices are not tuple[str, ...].
            ValueError: The choices are invalid.

        Returns:
            HandNames: The validated choices.
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

    def generate_choice_keys(self) -> list[str]:
        """Select a unique menu option for each Hand name.

        Currently, we use the uppercase first letter of the name, which
        must be unique.
        """
        return [choice[0].upper() for choice in self.names]

    @property
    def names(self) -> HandNames:
        """Tuple of game choices.

        By default, this returns the strings 'Rock', 'Paper', 'Scissors' from
        DEFAULT_CHOICE_NAMES. If you wish to modify the available choices, ensure
        that you validate them by running the `test_default_choices.py` pytest.

        Returns:
            HandNames: The game choice names.
        """
        return self._hand_names

    @property
    def choice_keys(self) -> list[str]:
        """Return list of menu options."""
        return self._choice_keys

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
    def is_beaten_by(self) -> dict[str, list[str]]:
        """A dictionary defines which _hands are beaten by each choice.

        Dictionary in the form: {winner: list[losers], ...}
        """
        return self._cyclic_hierarchy_map

    def _map_initial_to_name(self) -> dict[str, str]:
        """Map uppercase initial letter of name in choices, to name."""
        return {name[0].upper(): name for name in self.names}

    def _map_cyclic_hierarchy(self) -> dict[str, list[str]]:
        """Return dict mapping each choice to a list of choices that it beats."""
        number_of_beaten = (len(self._hand_names) - 1) // 2
        hierarchy_map = {}
        for idx, choice in enumerate(self.names):
            beaten = [self._hand_names[idx - j - 1] for j in range(number_of_beaten)]
            hierarchy_map[choice] = beaten
        return hierarchy_map


class UI:
    """Manages user interface ui.

    This version of Rock Scissors Paper implements a simple text interface in
    a Terminal window.
    """

    def __init__(self, config: GameOptions) -> None:
        """Initialise user interface.

        Args:
            config (GameOptions): Game choices and derived constants.
        """
        self.names = config.names
        self._menu_options: list[str] = config.choice_keys

    def get_user_input(self) -> str:
        """Prompt user for input."""
        prompt = (f"{self._format_choices()}, "
                  f"or [{QUIT_KEY}] to quit: ")
        return input(prompt).strip().upper()

    def _format_choices(self) -> str:
        """Return formatted string of choices.

        Formatted string in the form:
            '[R]ock, [S]cissors, [P]aper'
        """
        return ', '.join([f"[{name[0].upper()}]{name[1:]}"
                          for name in self.names])

    def invalid_choice(self):
        """Display invalid choice message."""
        choice_str = ', '.join([f"'{option}'" for option in self._menu_options])
        print(f"Invalid choice. Must be one of: {choice_str}.")

    def display_result(self, game_score: Scores,
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
        self.clear_screen()

        if player != '':
            print(f"You = {player} : "
                  f"Computer = {robo} : YOU {result_str}")
        print(f"Player: {game_score.player} | Computer: {game_score.robo}\n")

    @staticmethod
    def exit_message() -> None:
        """Display exit message."""
        print("Bye")

    @staticmethod
    def clear_screen() -> None:
        """Clear Terminal ui."""
        if 'TERM' in os.environ:
            # Should work cross-platform for most terminals.
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            print('\n')  # In Thonny we settle for a new line.
            # Escape codes may work for other Terminal emulators.
            print("\n\033[H\033[J", end="")


class Hand:
    """Hand objects represent the hand gestures made by players of this game.

    Each "hand" object  has a:

    - name (such as "Rock")
    - menu name ("[R]ock")
    - user choice name ("R")
    - "is_beaten_by" property (a list of other "_hands").
    """

    def __init__(self, options: GameOptions, hand_choice: str) -> None:
        """Instantiate a hand from hand_choice.

        Args:
            options (GameOptions): Configuration object of choices for current game.
            hand_choice (str): The kind of hand required. This may be the hand name
                (eg "Rock") or the hand choice key (eg "R").
        """
        self._options = options
        self.choice_key = None
        self.name = None
        self.is_beaten_by = options.is_beaten_by
        self.validate_choice(hand_choice)

        self.beaten_by = None

    def validate_choice(self, choice):
        """Validate hand_choice and assign self.name and self.choice_key.

        Args:
            choice (str): The user's  choice. This may be the name or choice_key.

        Raises:
            ValueError: If the user's choice is not valid.
        """
        if choice in self._options.choice_keys:
            self.choice_key = choice
            self.name = self._options.choice_map[choice]
        elif choice in self._options.names:
            self.name = choice
            self.choice_key = self._options.reverse_choice_map[choice]
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
        """Hand considered equal if name the same."""
        if isinstance(other, Hand):
            return self.name == other.name
        return False


class HandsFactory:
    """Factory for creating and managing Hand objects."""

    def __init__(self, options: GameOptions):
        """Initialize the factory with game _options."""
        self._options: GameOptions = options
        self._names: tuple[str, ...] = options.names
        self._beaten_by: dict[str, list[str]] = self._options.is_beaten_by

        # Create list of available Hand instances.
        self._hands = [Hand(options, name) for name in options.names]
        self._hands_by_name = {hand.name: hand for hand in self._hands}

        self._update_hand_properties()

    @property
    def hands(self) -> list[Hand]:
        """Return configured list of Hand objects.

        Used by robo_choice().
        """
        return self._hands

    def get_hand_by_name(self, name: str) -> Hand:
        """Return the Hand that has supplied name.

        Used by: player_choice().

        Raises:
            KeyError: If name is not a valid Hand name.

        Returns:
            Hand: The requested Hand.
        """
        return self._hands_by_name[name]

    def _update_hand_properties(self) -> None:
        """Populate the properties of each Hand."""
        for hand in self._hands:
            hand.is_beaten_by = self._get_beaten_by_list(hand)

    def _get_beaten_by_list(self, hand: Hand) -> list[Hand]:
        """Set the Hand's 'is_beaten_by' property."""
        beaten_by_names = self._beaten_by[hand.name]
        return [self.get_hand_by_name(name)
                for idx, name in enumerate(beaten_by_names)]


def player_choice(config: GameOptions, ui: UI) -> Hand:
    """Prompt and return human's hand gesture object.

    Returns:
        Hand: The selected Hand() object.
    """
    while True:
        choice = ui.get_user_input()

        if QUIT_KEY == choice:
            quit_game(ui)

        try:
            return Hand(config, choice)
        except ValueError:
            ui.invalid_choice()


def robo_choice(config: GameOptions) -> Hand:
    """Return a randomly selected hand gesture object.

    Args:
        config (GameOptions): The game configuration.

    Returns:
        Hand: The randomly selected hand object.
    """
    return Hand(config, random.choice(config.names))


def quit_game(ui: UI):
    """Exit the game and terminate the program."""
    ui.exit_message()
    sys.exit(0)


def main(config: GameOptions, ui: UI):
    """Game loop."""
    scores = Scores()
    ui.display_result(scores)
    _factory = HandsFactory(config)

    # Not yet used.
    hands = _factory.hands
    logging.debug(f"Hands: {hands}")

    while True:
        player_hand: Hand = player_choice(config, ui)
        robo_hand: Hand = robo_choice(config)

        if player_hand == robo_hand:
            ui.display_result(scores, player_hand.name, robo_hand.name, "DRAW")

        elif player_hand.beats(robo_hand):
            scores.player += 1
            ui.display_result(scores, player_hand.name, robo_hand.name, "WIN")

        else:
            scores.robo += 1
            ui.display_result(scores, player_hand.name, robo_hand.name, "LOSE")


if __name__ == '__main__':
    default_config = GameOptions(DEFAULT_CHOICE_NAMES)
    display_manager = UI(default_config)
    main(default_config, display_manager)
