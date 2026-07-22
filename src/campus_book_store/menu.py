from enum import Enum, auto

from . import helpers as helper


class Option(Enum):
    """Represent the available campus bookstore menu options.

    Each member's value is automatically assigned as an integer beginning
    with 1.

    Examples:
        Create an option from its numeric menu value:

        >>> Option(1)
        <Option.ADD_PRODUCT: 1>

        Access an option's numeric value:

        >>> Option.EXIT.value
        5
    """

    ADD_PRODUCT = auto()
    DISPLAY_ALL_PRODUCTS = auto()
    SEARCH_FOR_PRODUCT = auto()
    DISPLAY_INVENTORY_REPORT = auto()
    EXIT = auto()

    @property
    def label(self) -> str:
        """Return the option name formatted as a readable menu label.

        Underscores are replaced with spaces, and each word is converted
        to title case.

        Returns:
            str: The formatted label for the menu option.

        Examples:
            >>> Option.ADD_PRODUCT.label
            'Add Product'

            >>> Option.DISPLAY_INVENTORY_REPORT.label
            'Display Inventory Report'
        """
        return self.name.replace("_", " ").title()


def select_option(option: Option) -> None:
    """Run the function associated with a menu option.

    Args:
        option (Option): The menu option to run.

    Raises:
        ValueError: If `option` is not a recognized `Option` member.

    Examples:
        Selecting the exit option returns without performing an action:

        >>> select_option(Option.EXIT)

        A numeric value can first be converted into an `Option`:

        >>> selection = Option(5)
        >>> select_option(selection)
    """
    match option:
        case Option.ADD_PRODUCT:
            ...

        case Option.DISPLAY_ALL_PRODUCTS:
            ...

        case Option.SEARCH_FOR_PRODUCT:
            ...

        case Option.DISPLAY_INVENTORY_REPORT:
            ...

        case Option.EXIT:
            return

        case _:
            raise ValueError(f"Unknown option: {option}")


def get_menu_text() -> str:
    """Create and return the formatted menu text.

    Each menu option is placed on a separate line with its numeric value
    followed by its readable label.

    Returns:
        str: The complete formatted menu.

    Examples:
        >>> print(get_menu_text())
        1. Add Product
        2. Display All Products
        3. Search For Product
        4. Display Inventory Report
        5. Exit
    """
    return "\n".join(f"{option.value}. {option.label}" for option in Option)


def print_and_make_selection(number: int | str | None = None) -> None:
    """Display the menu, obtain a selection, and run the selected option.

    A supplied selection can be a number, a numeric string, or an unambiguous
    partial or fuzzy match for an option label. When no selection is supplied,
    the user is prompted until a valid selection is entered.

    Args:
        number (int | str | None): An optional numeric or text menu selection.
            When `None`, input is requested from the user. Defaults to `None`.

    Returns:
        None: The selected function is run, or the function returns after an
        invalid argument is supplied.

    Examples:
        Pass the exit option directly:

        >>> print_and_make_selection(5)
        1. Add Product
        2. Display All Products
        3. Search For Product
        4. Display Inventory Report
        5. Exit

        Numeric strings are also accepted:

        >>> print_and_make_selection("5")
        1. Add Product
        2. Display All Products
        3. Search For Product
        4. Display Inventory Report
        5. Exit

        Unambiguous partial text is accepted:

        >>> print_and_make_selection("exit")
        1. Add Product
        2. Display All Products
        3. Search For Product
        4. Display Inventory Report
        5. Exit
    """
    menu_text = get_menu_text()
    print(menu_text)

    while True:
        raw_selection = helper.input_or_arg(
            number,
            "Select an option: ",
        )

        try:
            selection = Option(int(raw_selection))
        except (TypeError, ValueError):
            selection = helper.interpret_partial_text(
                str(raw_selection),
                Option,
                label=lambda option: option.label,
            )

        if selection is None:
            print(
                f"{raw_selection!r} is not an unambiguous menu option."
                f"\n{menu_text}"
            )

            if number is not None:
                return

            continue

        select_option(selection)
        return


def main() -> None:
    """Run the campus bookstore menu.

    The user is shown the menu and prompted to select an option.

    Examples:
        The application can be started from the command line with:

        `python -m campus_book_store`

        It can also be started using the installed project command:

        `campus-book-store`
    """
    print_and_make_selection()


if __name__ == "__main__":
    main()
