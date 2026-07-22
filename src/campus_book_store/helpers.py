"""
Name: Derek R. Neilson
Description: Helper functions for my project
"""

from collections.abc import Callable, Iterable
from difflib import SequenceMatcher
from typing import TypeVar
import re
import shutil

T = TypeVar("T")  # "T" can be any type. This is used for type hinting purposes.


def input_or_arg(argument: T | None, prompt: str) -> T | str:
    """Return the supplied argument or prompt the user when it is None.

    Args:
        argument (T | None): A variable of any type.
        prompt (str): The prompt displayed when `argument` is `None`.

    Returns:
        T | str: The supplied argument or the user's response.

    Examples:
        >>> event_type = "Book Sale"
        >>> input_or_arg(event_type, "What is the event type: ")
        'Book Sale'
    """
    if argument is not None:
        return argument

    return input(prompt)


def _normalize_text(text: str) -> str:
    """Normalize text so that it can be compared consistently.

    The text is converted to lowercase, punctuation is removed, and
    repeated whitespace is reduced to single spaces.

    Args:
        text (str): The text to normalize.

    Returns:
        str: The normalized text.

    Examples:
        >>> _normalize_text("  Add-Product! ")
        'add product'
    """
    words = re.findall(r"[a-z0-9]+", text.lower())
    return " ".join(words)


def interpret_partial_text(
    text: str,
    options: Iterable[T],
    *,
    label: Callable[[T], str] = str,
    cutoff: float = 0.65,
) -> T | None:
    """Find one unambiguous option matching partial or misspelled text.

    Matching is performed in the following order:

    1. Exact normalized match.
    2. Unique partial-word match.
    3. Unique fuzzy match.

    A partial word can match the beginning of a word in an option. For
    example, `"disp all"` matches `"Display All Products"`.

    If the text matches multiple options, no selection is made and `None`
    is returned.

    Args:
        text (str): The partial or potentially misspelled user input.
        options (Iterable[T]): The available values that may be selected.
        label (Callable[[T], str]): A function that returns the readable
            label for each option. Defaults to `str`.
        cutoff (float): The minimum fuzzy-match score, from 0.0 to 1.0.
            Defaults to 0.65.

    Returns:
        T | None: The single matching option, or `None` when there is no
        match or the result is ambiguous.

    Raises:
        ValueError: If `cutoff` is outside the range 0.0 through 1.0.

    Examples:
        >>> choices = [
        ...     "Add Product",
        ...     "Display All Products",
        ...     "Search for a Product",
        ...     "Display Inventory Report",
        ...     "Exit",
        ... ]

        A unique partial option is selected:

        >>> interpret_partial_text("add", choices)
        'Add Product'

        Multiple partial matches are considered ambiguous:

        >>> interpret_partial_text("display", choices) is None
        True

        Multiple options containing "product" are also ambiguous:

        >>> interpret_partial_text("product", choices) is None
        True

        Multiple abbreviated words can identify one option:

        >>> interpret_partial_text("disp all", choices)
        'Display All Products'

        Minor spelling mistakes can be interpreted:

        >>> interpret_partial_text("inventry report", choices)
        'Display Inventory Report'

        Unrecognized input returns `None`:

        >>> interpret_partial_text("remove", choices) is None
        True
    """
    if not 0.0 <= cutoff <= 1.0:
        raise ValueError("cutoff must be between 0.0 and 1.0")

    normalized_text = _normalize_text(text)

    if not normalized_text:
        return None

    candidates = [(option, _normalize_text(label(option))) for option in options]

    exact_matches = [
        option
        for option, normalized_label in candidates
        if normalized_label == normalized_text
    ]

    if len(exact_matches) == 1:
        return exact_matches[0]

    if len(exact_matches) > 1:
        return None

    query_words = normalized_text.split()
    partial_matches: list[T] = []

    for option, normalized_label in candidates:
        option_words = normalized_label.split()

        all_words_match = all(
            any(option_word.startswith(query_word) for option_word in option_words)
            for query_word in query_words
        )

        if all_words_match:
            partial_matches.append(option)

    if len(partial_matches) == 1:
        return partial_matches[0]

    if len(partial_matches) > 1:
        return None

    fuzzy_matches = [
        option
        for option, normalized_label in candidates
        if SequenceMatcher(
            None,
            normalized_text,
            normalized_label,
        ).ratio()
        >= cutoff
    ]

    if len(fuzzy_matches) == 1:
        return fuzzy_matches[0]

    return None


def yes_or_no(prompt: str, value: bool | None = None) -> bool:
    """Return the supplied Boolean or request a yes-or-no response.

    Args:
        prompt (str): The message displayed when requesting input.
        value (bool | None): A Boolean value. When `None`, the user is
            prompted. Defaults to `None`.

    Returns:
        bool: `True` for yes and `False` for no.

    Raises:
        TypeError: If `value` is not a Boolean or `None`.

    Examples:
        >>> yes_or_no(
        ...     "Do you consent to have your directory scanned? ",
        ...     True,
        ... )
        True

        >>> yes_or_no("Continue? ", False)
        False
    """
    if isinstance(value, bool):
        return value

    if value is not None:
        raise TypeError("value must be a Boolean or None")

    while True:
        response = input(prompt).strip().lower()

        if response in ("yes", "y"):
            return True

        if response in ("no", "n"):
            return False

        print("Please enter yes or no.")


terminal_width: int = shutil.get_terminal_size(fallback=(120, 30)).columns
