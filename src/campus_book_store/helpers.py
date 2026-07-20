"""
Name: Derek R. Neilson
Description: Helper functions for my project
"""

from typing import TypeVar
import shutil

T = TypeVar(
    "T"
)  # "T" can be any type. Note this is purely for stylistic and type hinting purposes


def input_or_arg(argument: T | None, prompt: str) -> T | str:
    """Return the supplied argument or prompt the user when it is None.

    Args:
        argument (T | None): a variable with any type
        prompt (str): the prompt if `argument` is `None`

    Returns:
        T | str:  a variable with any type

    Example:
        >>> event_type = "Book Sale"
        >>> input_or_arg(event_type, "What is the event type: ")
        'Book Sale'
    """
    if argument is not None:
        return argument

    return input(prompt)


def yes_or_no(prompt: str, value: bool | None = None) -> bool:
    """
    Return the supplied Boolean, or ask the user for a yes-or-no response.

    Args:
        prompt: The message displayed when requesting input.
        value: A Boolean value. When None, the user is prompted.

    Returns:
        True for yes and False for no.

    Raises:
        TypeError: If value is not a Boolean or None.

    Example:
        >>> yes_or_no("Do you consent to have your directory scanned? ", True)
        True
    """
    if isinstance(
        value, bool
    ):  # `isinstance(value, bool)` checks whether value is a Boolean preferred over `type()` because it respects inheritance.
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


terminal_width: int = shutil.get_terminal_size(
    fallback=(120, 30)
).columns  # I remember using this at one point.
# but honestly I dont know why it is in `shutil` instead of `os` but the `os` one fallback dose not return a int
