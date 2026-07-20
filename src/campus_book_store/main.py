from . import helpers as helper


def main() -> None:
    """Run the lab program."""
    separator: str = "=" * helper.terminal_width
    sub_separator: str = "-" * helper.terminal_width
    print("Hello welcome to the CLI for the campus book store!")


if __name__ == "__main__":
    main()
