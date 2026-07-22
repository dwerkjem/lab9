"""Tests for the Campus Bookstore Inventory System."""

import pytest

from campus_book_store import inventory as store
from campus_book_store import menu


def test_add_product_uses_required_collections(capsys: pytest.CaptureFixture[str]) -> None:
    inventory: store.Inventory = {}
    categories: set[str] = set()

    added = store.add_product(
        "b101",
        "Python Programming",
        "Books",
        "79.95",
        "12",
        inventory_data=inventory,
        categories_data=categories,
    )

    assert added is True
    assert inventory == {
        "B101": ("Python Programming", "Books", 79.95, 12)
    }
    assert isinstance(inventory["B101"], tuple)
    assert categories == {"Books"}
    assert "Product added successfully." in capsys.readouterr().out


def test_duplicate_product_id_is_rejected(capsys: pytest.CaptureFixture[str]) -> None:
    inventory: store.Inventory = {
        "B101": ("Python Programming", "Books", 79.95, 12)
    }
    categories = {"Books"}

    added = store.add_product(
        "b101",
        "Another Book",
        "Books",
        20,
        3,
        inventory_data=inventory,
        categories_data=categories,
    )

    assert added is False
    assert len(inventory) == 1
    assert "already exists" in capsys.readouterr().out


def test_duplicate_categories_are_not_stored() -> None:
    inventory: store.Inventory = {}
    categories: set[str] = set()

    store.add_product(
        "B101",
        "Python",
        "Books",
        10,
        2,
        inventory_data=inventory,
        categories_data=categories,
    )
    store.add_product(
        "B102",
        "Algorithms",
        "Books",
        15,
        8,
        inventory_data=inventory,
        categories_data=categories,
    )

    assert categories == {"Books"}


def test_search_by_product_id_is_case_insensitive(
    capsys: pytest.CaptureFixture[str],
) -> None:
    inventory: store.Inventory = {
        "P205": ("Pens", "School Supplies", 2.5, 10)
    }

    product = store.search_product(" p205 ", inventory_data=inventory)

    assert product == ("Pens", "School Supplies", 2.5, 10)
    assert "P205" in capsys.readouterr().out


def test_missing_product_displays_message(capsys: pytest.CaptureFixture[str]) -> None:
    result = store.search_product("X999", inventory_data={})

    assert result is None
    assert "Product ID X999 was not found." in capsys.readouterr().out


def test_low_stock_products_are_stored_in_a_list() -> None:
    inventory: store.Inventory = {
        "B101": ("Python", "Books", 79.95, 12),
        "P205": ("Pens", "School Supplies", 2.5, 4),
        "S310": ("Notebook", "School Supplies", 5.0, 0),
        "E100": ("Calculator", "Electronics", 20.0, 5),
    }

    low_stock = store.build_reorder_list(inventory)

    assert isinstance(low_stock, list)
    assert low_stock == ["P205", "S310"]


def test_inventory_report_has_required_summary(
    capsys: pytest.CaptureFixture[str],
) -> None:
    inventory: store.Inventory = {
        "B101": ("Python", "Books", 10.0, 2),
        "P205": ("Pens", "School Supplies", 1.5, 4),
    }
    categories = {"Books", "School Supplies"}

    report = store.display_inventory_report(inventory, categories)

    assert "Total number of products: 2" in report
    assert "Categories: Books, School Supplies" in report
    assert "Low Stock (quantity below 5): B101, P205" in report
    assert "Total inventory value: $26.00" in report
    assert report in capsys.readouterr().out


def test_display_all_products_formats_inventory(
    capsys: pytest.CaptureFixture[str],
) -> None:
    inventory: store.Inventory = {
        "B101": ("Python Programming", "Books", 79.95, 12)
    }

    output = store.display_all_products(inventory)

    assert "Product ID" in output
    assert "Python Programming" in output
    assert "$     79.95" in output
    assert output in capsys.readouterr().out


def test_invalid_price_and_quantity_are_rejected() -> None:
    with pytest.raises(ValueError, match="Price cannot be negative"):
        store.add_product("B101", "Python", "Books", -1, 1)

    with pytest.raises(ValueError, match="Quantity must be a whole number"):
        store.add_product("B102", "Python", "Books", 1, "3.5")


def test_all_menu_options_dispatch(monkeypatch: pytest.MonkeyPatch) -> None:
    called: list[str] = []

    monkeypatch.setattr(store, "add_product", lambda: called.append("add"))
    monkeypatch.setattr(
        store,
        "display_all_products",
        lambda: called.append("display"),
    )
    monkeypatch.setattr(store, "search_product", lambda: called.append("search"))
    monkeypatch.setattr(
        store,
        "display_inventory_report",
        lambda: called.append("report"),
    )

    assert menu.select_option(menu.Option.ADD_PRODUCT) is True
    assert menu.select_option(menu.Option.DISPLAY_ALL_PRODUCTS) is True
    assert menu.select_option(menu.Option.SEARCH_FOR_PRODUCT) is True
    assert menu.select_option(menu.Option.DISPLAY_INVENTORY_REPORT) is True
    assert menu.select_option(menu.Option.EXIT) is False
    assert called == ["add", "display", "search", "report"]


def test_fuzzy_menu_selection_is_unique() -> None:
    assert menu.interpret_selection("add") is menu.Option.ADD_PRODUCT
    assert menu.interpret_selection("disp all") is menu.Option.DISPLAY_ALL_PRODUCTS
    assert menu.interpret_selection("inventry report") is menu.Option.DISPLAY_INVENTORY_REPORT
    assert menu.interpret_selection("display") is None
