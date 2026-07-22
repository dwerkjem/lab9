# Campus Bookstore Inventory System

**Student:** Derek R. Neilson  
**Course:** Programming 1  
**Lab:** Lab 9

A command-line inventory system that stores bookstore products, prevents duplicate
Product IDs and categories, searches by Product ID, identifies low-stock products,
and calculates total inventory value.

## Program design

- Product ID is the unique dictionary key.
- Product name, category, price, and quantity are stored together in a tuple.
- Categories are stored in a set so duplicates are automatically removed.
- Product IDs with quantities below five are stored in a reorder list.
- The menu remains active through a `while` loop until Exit is selected.
- Numeric, partial, and unambiguous fuzzy menu selections are accepted.

## Set up the project

```bash
uv sync --dev
uv run pre-commit install
```

## Run the project

```bash
uv run campus-book-store
```

The package can also be run directly:

```bash
uv run python -m campus_book_store
```

## Run the tests

```bash
uv run pytest
```

The test suite includes more than the five required test cases and covers every
menu option, adding products, duplicate IDs and categories, Product ID searches,
input validation, low-stock products, formatted output, and report totals.

## Format the code

```bash
uv run black .
uv run pre-commit run --all-files
```
