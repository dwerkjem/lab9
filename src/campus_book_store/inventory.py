"""Store and process products for the campus bookstore inventory system."""

from . import helpers as helper

Product = tuple[str, str, float, int]
Inventory = dict[str, Product]

LOW_STOCK_THRESHOLD = 5

# The assignment requires a dictionary, tuple, set, and list. These collections
# hold the inventory for the duration of the running program.
inventory: Inventory = {}
categories: set[str] = set()
reorder_products: list[str] = []


def clear_inventory() -> None:
    """Remove all products and derived collection values.

    This is primarily useful when starting a new session or isolating tests.

    Examples:
        >>> inventory["B101"] = ("Python", "Books", 10.0, 1)
        >>> categories.add("Books")
        >>> reorder_products.append("B101")
        >>> clear_inventory()
        >>> inventory
        {}
        >>> categories
        set()
        >>> reorder_products
        []
    """
    inventory.clear()
    categories.clear()
    reorder_products.clear()


def normalize_product_id(product_id: object) -> str:
    """Return a trimmed, uppercase Product ID.

    Args:
        product_id (object): The value to normalize.

    Returns:
        str: The normalized Product ID.

    Examples:
        >>> normalize_product_id(" b101 ")
        'B101'
    """
    return str(product_id).strip().upper()


def _read_required_text(
    value: object | None,
    prompt: str,
    field_name: str,
) -> str:
    """Read a non-empty text value from an argument or interactive input."""
    while True:
        raw_value = helper.input_or_arg(value, prompt)
        text = str(raw_value).strip()

        if text:
            return text

        message = f"{field_name} cannot be blank."
        if value is not None:
            raise ValueError(message)

        print(message)


def _read_price(value: object | None, prompt: str = "Enter Price: ") -> float:
    """Read and validate a non-negative product price."""
    while True:
        raw_value = helper.input_or_arg(value, prompt)

        try:
            price = float(raw_value)
        except (TypeError, ValueError):
            message = "Price must be a number."
        else:
            if price >= 0:
                return price
            message = "Price cannot be negative."

        if value is not None:
            raise ValueError(message)

        print(message)


def _read_quantity(
    value: object | None,
    prompt: str = "Enter Quantity: ",
) -> int:
    """Read and validate a non-negative whole-number quantity."""
    while True:
        raw_value = helper.input_or_arg(value, prompt)

        try:
            if isinstance(raw_value, bool):
                raise ValueError
            quantity = int(str(raw_value).strip())
        except (TypeError, ValueError):
            message = "Quantity must be a whole number."
        else:
            if quantity >= 0:
                return quantity
            message = "Quantity cannot be negative."

        if value is not None:
            raise ValueError(message)

        print(message)


def build_reorder_list(inventory_data: Inventory | None = None) -> list[str]:
    """Create a list of Product IDs whose quantity is less than five.

    Args:
        inventory_data (Inventory | None): Inventory to examine. The program's
            shared inventory is used when omitted.

    Returns:
        list[str]: Product IDs that need to be reordered.

    Examples:
        >>> sample = {
        ...     "B101": ("Python", "Books", 79.95, 12),
        ...     "P205": ("Pens", "School Supplies", 2.50, 4),
        ... }
        >>> build_reorder_list(sample)
        ['P205']
    """
    data = inventory if inventory_data is None else inventory_data
    return [
        product_id
        for product_id, product in data.items()
        if product[3] < LOW_STOCK_THRESHOLD
    ]


def _refresh_reorder_products(inventory_data: Inventory | None = None) -> list[str]:
    """Synchronize the required low-stock list with the inventory."""
    reorder_products.clear()
    reorder_products.extend(build_reorder_list(inventory_data))
    return reorder_products


def add_product(
    product_id: object | None = None,
    name: object | None = None,
    category: object | None = None,
    price: object | None = None,
    quantity: object | None = None,
    *,
    inventory_data: Inventory | None = None,
    categories_data: set[str] | None = None,
) -> bool:
    """Prompt for and add one unique product to the inventory.

    The dictionary key is the Product ID. Its value is a tuple containing the
    product name, category, price, and quantity. The category is also added to
    the category set.

    Args:
        product_id: Optional Product ID used instead of prompting.
        name: Optional product name used instead of prompting.
        category: Optional category used instead of prompting.
        price: Optional price used instead of prompting.
        quantity: Optional quantity used instead of prompting.
        inventory_data: Optional inventory dictionary used for testing.
        categories_data: Optional category set used for testing.

    Returns:
        bool: `True` when the product is added, otherwise `False` for a
        duplicate Product ID.

    Raises:
        ValueError: If a supplied argument is blank or numerically invalid.

    Examples:
        >>> sample_inventory = {}
        >>> sample_categories = set()
        >>> add_product(
        ...     "B101", "Python Programming", "Books", 79.95, 12,
        ...     inventory_data=sample_inventory,
        ...     categories_data=sample_categories,
        ... )
        Product added successfully.
        True
        >>> sample_inventory["B101"]
        ('Python Programming', 'Books', 79.95, 12)
        >>> sample_categories
        {'Books'}
    """
    data = inventory if inventory_data is None else inventory_data
    category_set = categories if categories_data is None else categories_data

    normalized_id = normalize_product_id(
        _read_required_text(product_id, "Enter Product ID: ", "Product ID")
    )

    if normalized_id in data:
        print(f"Product ID {normalized_id} already exists.")
        return False

    product_name = _read_required_text(name, "Enter Product Name: ", "Product name")
    product_category = _read_required_text(
        category,
        "Enter Category: ",
        "Category",
    )
    product_price = _read_price(price)
    product_quantity = _read_quantity(quantity)

    # A tuple groups the four values describing one product.
    data[normalized_id] = (
        product_name,
        product_category,
        product_price,
        product_quantity,
    )
    category_set.add(product_category)

    if data is inventory:
        _refresh_reorder_products()

    print("Product added successfully.")
    return True


def _product_table(inventory_data: Inventory) -> str:
    """Return a formatted table containing every supplied product."""
    header = (
        f"{'Product ID':<12} {'Product Name':<30} {'Category':<22} "
        f"{'Price':>12} {'Quantity':>10}"
    )
    separator = "-" * len(header)
    rows = [header, separator]

    for product_id, (name, category, price, quantity) in sorted(
        inventory_data.items()
    ):
        rows.append(
            f"{product_id:<12} {name:<30.30} {category:<22.22} "
            f"${price:>10,.2f} {quantity:>10,d}"
        )

    return "\n".join(rows)


def display_all_products(inventory_data: Inventory | None = None) -> str:
    """Display every product currently stored in the inventory.

    Args:
        inventory_data (Inventory | None): Inventory to display. The program's
            shared inventory is used when omitted.

    Returns:
        str: The displayed table or an empty-inventory message.
    """
    data = inventory if inventory_data is None else inventory_data

    if not data:
        output = "No products are currently in the inventory."
    else:
        output = f"All Products\n{'=' * 12}\n{_product_table(data)}"

    print(output)
    return output


def search_product(
    product_id: object | None = None,
    *,
    inventory_data: Inventory | None = None,
) -> Product | None:
    """Search for and display a product using its Product ID.

    Args:
        product_id: Optional Product ID used instead of prompting.
        inventory_data: Optional inventory dictionary used for testing.

    Returns:
        Product | None: The matching product tuple, or `None` when not found.
    """
    data = inventory if inventory_data is None else inventory_data
    requested_id = normalize_product_id(
        _read_required_text(product_id, "Enter Product ID: ", "Product ID")
    )
    product = data.get(requested_id)

    if product is None:
        print(f"Product ID {requested_id} was not found.")
        return None

    print(_product_table({requested_id: product}))
    return product


def calculate_total_inventory_value(
    inventory_data: Inventory | None = None,
) -> float:
    """Calculate the price times quantity for every product.

    A dictionary comprehension creates a per-product value mapping before the
    values are totaled.

    Args:
        inventory_data (Inventory | None): Inventory to total.

    Returns:
        float: Total monetary value of all units in stock.

    Examples:
        >>> calculate_total_inventory_value({
        ...     "B101": ("Python", "Books", 10.0, 2),
        ...     "P205": ("Pens", "Supplies", 1.5, 4),
        ... })
        26.0
    """
    data = inventory if inventory_data is None else inventory_data
    product_values = {
        product_id: product[2] * product[3]
        for product_id, product in data.items()
    }
    return sum(product_values.values())


def display_inventory_report(
    inventory_data: Inventory | None = None,
    categories_data: set[str] | None = None,
) -> str:
    """Display the required inventory summary report.

    The report includes product count, unique categories, low-stock products,
    and total inventory value.

    Args:
        inventory_data (Inventory | None): Inventory to summarize.
        categories_data (set[str] | None): Categories to display.

    Returns:
        str: The formatted report text.
    """
    data = inventory if inventory_data is None else inventory_data
    category_set = categories if categories_data is None else categories_data
    low_stock = build_reorder_list(data)

    if data is inventory:
        _refresh_reorder_products()

    category_text = ", ".join(sorted(category_set)) if category_set else "None"
    low_stock_text = ", ".join(low_stock) if low_stock else "None"

    lines = [
        "Inventory Report",
        "=" * 16,
        f"Total number of products: {len(data)}",
        f"Categories: {category_text}",
        f"Low Stock (quantity below {LOW_STOCK_THRESHOLD}): {low_stock_text}",
        f"Total inventory value: ${calculate_total_inventory_value(data):,.2f}",
    ]
    output = "\n".join(lines)
    print(output)
    return output
