from . import helpers as helper
from .menu import print_and_make_selection


def main() -> None:
    """Run the lab program."""
    separator: str = "=" * helper.terminal_width
    sub_separator: str = "-" * helper.terminal_width
    print("Hello welcome to the CLI for the campus book store!")
    print(separator)
    print_and_make_selection()


if __name__ == "__main__":
    main()
