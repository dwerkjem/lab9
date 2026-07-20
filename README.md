# Campus book store

**Student:** Derek R. Neilson  
**Course:** Programming 1  
**Lab:** Lab 9 — A simple inventory system for the campus bookstore, built to meet the specified requirements.

A simple inventory system for the campus bookstore, built to meet the specified requirements.


## Set up the project

```bash
git init
uv sync --dev
uv run pre-commit install
```

## Run the project

```bash
uv run campus-book-store
```

## Run the tests

```bash
uv run pytest
```

## Format the code

```bash
uv run black .
uv run pre-commit run --all-files
```

The pre-commit hook only formats Python files with Black. It does not lint the
code or enforce additional style rules.