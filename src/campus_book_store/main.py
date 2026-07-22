"""Application entry point for the campus bookstore inventory system."""

from . import helpers as helper
from .menu import print_and_make_selection


def main() -> None:
    """Run the campus bookstore inventory system."""
    title = "Campus Bookstore Inventory System"
    separator = "=" * min(len(title), helper.terminal_width)
    print(title)
    print(separator)
    print_and_make_selection()


if __name__ == "__main__":
    main()
