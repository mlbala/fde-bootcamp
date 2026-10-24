"""Session 05 project 5: a supermarket billing system (topics 1-3).

Brings all of the session's topics together:
- String formatting: the receipt uses str.format() and most of the format spec
  mini-language (alignment, width, thousands separator, precision, %, zero padding,
  dates, cutting long text, a dynamic width, and a template filled with **)
- Dicts as hash tables: the product catalog and the cart, both keyed by product code
- if / elif / else: the discount slabs, where the order of the conditions matters
- while and for loops, and functions that return values
- Copying: cart.copy() so a finished bill isn't wiped out by cart.clear()

It only uses what was covered up to session 05, so there is no try / except
(that's session 06). The quantity is checked with isdecimal() before int().

Run it with:
    python Assignment/s05-python-2-hash/project-5/billing.py
"""

from datetime import datetime

STORE_NAME = "FDE SUPERMARKET"
WIDTH = 48
TAX_RATE = 0.05
MAX_QUANTITY = 99

# CATALOG["B1"] jumps straight to the product (a hash lookup), however big the catalog gets
CATALOG = {
    "A1": {"name": "Basmati rice 5kg", "price": 545.00},
    "A2": {"name": "Toor dal 1kg", "price": 168.00},
    "A3": {"name": "Sunflower oil 1L", "price": 152.50},
    "B1": {"name": "Milk 1L", "price": 66.00},
    "B2": {"name": "Paneer 200g", "price": 95.00},
    "B3": {"name": "Curd 500g", "price": 45.00},
    "C1": {"name": "Bath soap (pack of 4)", "price": 210.00},
    "C2": {"name": "Toothpaste 150g", "price": 99.00},
    "D1": {"name": "Notebook 200 pages", "price": 60.00},
    "D2": {"name": "Ball pen (pack of 10)", "price": 100.00},
}

# Templates for one row of the receipt: 24 + 5 + 9 + 10 = WIDTH characters.
# {:<24.24} pads the name to 24 characters AND cuts it if it's longer.
HEADER_ROW = "{:<24.24}{:>5}{:>9}{:>10}"
ITEM_ROW = "{:<24.24}{:>5}{:>9,.2f}{:>10,.2f}"
TOTAL_ROW = "{:<32}{:>16,.2f}"
FOOTER = "{items} items | You saved Rs {discount:,.2f} | Thank you!"


def discount_rate(subtotal):
    """Return the discount for a subtotal, e.g. 0.05 for 5%."""
    # Check the biggest slab first: if 1,000 came first, a 6,000 bill would only get 2%
    if subtotal >= 5000:
        return 0.10
    elif subtotal >= 2000:
        return 0.05
    elif subtotal >= 1000:
        return 0.02
    else:
        return 0.0


def clean_code(code):
    return code.strip().upper()


def parse_quantity(text):
    """Turn text into a quantity. Returns two values, (quantity, error)."""
    text = text.strip()
    # isdecimal(), not isdigit(): "²".isdigit() is True, but int("²") would crash
    if not text.isdecimal():
        return None, "quantity must be a whole number"
    quantity = int(text)
    if quantity < 1 or quantity > MAX_QUANTITY:
        return None, "quantity must be from 1 to {}".format(MAX_QUANTITY)
    return quantity, None


def add_to_cart(cart, code, quantity):
    """Add quantity of a product to the cart. Returns an error message, or None if it was added."""
    code = clean_code(code)
    if code not in CATALOG:
        return "no product with code '{}'".format(code)
    new_quantity = cart.get(code, 0) + quantity
    if new_quantity > MAX_QUANTITY:
        return "at most {} of one product per bill".format(MAX_QUANTITY)
    cart[code] = new_quantity
    return None


def remove_from_cart(cart, code):
    """Remove a product from the cart. Returns an error message, or None if it was removed."""
    code = clean_code(code)
    if code not in cart:
        return "'{}' is not in the cart".format(code)
    del cart[code]
    return None


def calculate_bill(cart):
    """Return every number the receipt needs, in one dict."""
    subtotal = 0
    items = 0
    for code, quantity in cart.items():
        subtotal += CATALOG[code]["price"] * quantity
        items += quantity

    # Round each step to paise, so the printed lines add up exactly to the printed total
    subtotal = round(subtotal, 2)
    rate = discount_rate(subtotal)
    discount = round(subtotal * rate, 2)
    tax = round((subtotal - discount) * TAX_RATE, 2)
    total = round(subtotal - discount + tax, 2)
    return {"items": items, "subtotal": subtotal, "rate": rate, "discount": discount, "tax": tax, "total": total}


def format_catalog():
    lines = ["{:<6}{:<26}{:>10}".format("Code", "Product", "Price")]
    for code, product in CATALOG.items():
        lines.append("{:<6}{:<26}{:>10,.2f}".format(code, product["name"], product["price"]))
    return "\n".join(lines)


def format_receipt(cart, customer, when, bill_number):
    """Return the whole receipt as one string."""
    bill = calculate_bill(cart)
    date_and_number = "{:%d-%m-%Y %H:%M}   Bill #{:04d}".format(when, bill_number)

    lines = [
        "=" * WIDTH,
        "{:^{width}}".format(STORE_NAME, width=WIDTH).rstrip(),  # the width comes from a variable
        "{:^{width}}".format(date_and_number, width=WIDTH).rstrip(),
        "=" * WIDTH,
        "Customer: {}".format(customer),
        "-" * WIDTH,
        HEADER_ROW.format("Item", "Qty", "Price", "Amount"),
    ]
    for code, quantity in cart.items():
        product = CATALOG[code]
        lines.append(ITEM_ROW.format(product["name"], quantity, product["price"], product["price"] * quantity))

    lines.append("-" * WIDTH)
    lines.append(TOTAL_ROW.format("Subtotal", bill["subtotal"]))
    if bill["discount"] > 0:
        lines.append(TOTAL_ROW.format("Discount ({:.0%})".format(bill["rate"]), -bill["discount"]))
    lines.append(TOTAL_ROW.format("Tax ({:.0%})".format(TAX_RATE), bill["tax"]))
    lines.append("=" * WIDTH)
    lines.append("{:<28}{:>20}".format("TOTAL", "Rs {:,.2f}".format(bill["total"])))
    lines.append("=" * WIDTH)
    lines.append("{:>{width}}".format(FOOTER.format(**bill), width=WIDTH))  # **bill fills {items} and {discount}
    return "\n".join(lines)


MENU = """
1. Show products
2. Add item
3. Remove item
4. View bill
5. Checkout
6. Close the counter"""


def main():
    cart = {}  # product code -> quantity
    finished_bills = []
    print("{:=^{width}}".format(" " + STORE_NAME + " BILLING ", width=WIDTH))

    while True:
        print(MENU)
        choice = input("Choose 1-6: ").strip()

        if choice == "1":
            print(format_catalog())

        elif choice == "2":
            code = input("Product code: ")
            quantity, error = parse_quantity(input("Quantity: "))
            if error is None:
                error = add_to_cart(cart, code, quantity)
            if error is None:
                product = CATALOG[clean_code(code)]
                print("  Added {} x {}".format(quantity, product["name"]))
            else:
                print("  " + error)

        elif choice == "3":
            error = remove_from_cart(cart, input("Product code: "))
            print("  " + (error if error is not None else "Removed."))

        elif choice == "4":
            if not cart:
                print("  The cart is empty.")
            else:
                print(format_receipt(cart, "(not checked out yet)", datetime.now(), len(finished_bills) + 1))

        elif choice == "5":
            if not cart:
                print("  The cart is empty.")
                continue
            customer = input("Customer name: ").strip() or "Guest"  # an empty string is falsy
            print(format_receipt(cart, customer, datetime.now(), len(finished_bills) + 1))
            # Save a COPY: cart.clear() empties this dict, and a saved reference would be emptied with it
            finished_bills.append({"customer": customer, "cart": cart.copy(), "total": calculate_bill(cart)["total"]})
            cart.clear()

        elif choice == "6":
            if cart:
                print("  Warning: the cart still has items that were never checked out.")
            sales = 0
            for bill in finished_bills:
                sales += bill["total"]
            print("Bills today: {}   Total sales: Rs {:,.2f}".format(len(finished_bills), sales))
            break

        else:
            print("Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
