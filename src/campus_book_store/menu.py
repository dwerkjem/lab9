"""Display and process the campus bookstore command-line menu."""

from enum import Enum, auto

from . import helpers as helper
from . import inventory as store


class Option(Enum):
    """Represent the available campus bookstore menu options.

    Examples:
        >>> Option(1)
        <Option.ADD_PRODUCT: 1>
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

        Examples:
            >>> Option.ADD_PRODUCT.label
            'Add Product'
            >>> Option.DISPLAY_INVENTORY_REPORT.label
            'Display Inventory Report'
        """
        return self.name.replace("_", " ").title()


def select_option(option: Option) -> bool:
    """Run the function associated with a menu option.

    Args:
        option (Option): The menu option to run.

    Returns:
        bool: `True` to continue showing the menu or `False` to exit.

    Raises:
        ValueError: If `option` is not a recognized `Option` member.

    Examples:
        >>> select_option(Option.EXIT)
        Goodbye!
        False
    """
    match option:
        case Option.ADD_PRODUCT:
            store.add_product()
        case Option.DISPLAY_ALL_PRODUCTS:
            store.display_all_products()
        case Option.SEARCH_FOR_PRODUCT:
            store.search_product()
        case Option.DISPLAY_INVENTORY_REPORT:
            store.display_inventory_report()
        case Option.EXIT:
            print("Goodbye!")
            return False
        case _:
            raise ValueError(f"Unknown option: {option}")

    return True


def get_menu_text() -> str:
    """Create and return the formatted menu text.

    Examples:
        >>> print(get_menu_text())
        1. Add Product
        2. Display All Products
        3. Search For Product
        4. Display Inventory Report
        5. Exit
    """
    return "\n".join(f"{option.value}. {option.label}" for option in Option)


def interpret_selection(raw_selection: object) -> Option | None:
    """Interpret a numeric, partial, or fuzzy menu selection.

    Args:
        raw_selection (object): User-entered menu choice.

    Returns:
        Option | None: A unique matching option, otherwise `None`.

    Examples:
        >>> interpret_selection(1)
        <Option.ADD_PRODUCT: 1>
        >>> interpret_selection("disp all")
        <Option.DISPLAY_ALL_PRODUCTS: 2>
        >>> interpret_selection("display") is None
        True
    """
    try:
        return Option(int(raw_selection))
    except (TypeError, ValueError):
        return helper.interpret_partial_text(
            str(raw_selection),
            Option,
            label=lambda option: option.label,
        )


def print_and_make_selection(number: int | str | None = None) -> None:
    """Display the menu and process selections until the user exits.

    A supplied value processes one menu selection and then returns. Without an
    argument, a while loop repeatedly prompts until Exit is selected.

    Args:
        number (int | str | None): Optional numeric, partial, or fuzzy choice.

    Examples:
        >>> print_and_make_selection("exit")
        1. Add Product
        2. Display All Products
        3. Search For Product
        4. Display Inventory Report
        5. Exit
        Goodbye!
    """
    menu_text = get_menu_text()

    while True:
        print(menu_text)
        raw_selection = helper.input_or_arg(number, "Enter your choice: ")
        selection = interpret_selection(raw_selection)

        if selection is None:
            print(f"{raw_selection!r} is not an unambiguous menu option.")

            if number is not None:
                return

            print()
            continue

        should_continue = select_option(selection)

        if number is not None or not should_continue:
            return

        print()


def main() -> None:
    """Run the campus bookstore menu."""
    print_and_make_selection()


if __name__ == "__main__":
    main()
