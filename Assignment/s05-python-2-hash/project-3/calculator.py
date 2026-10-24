"""Session 05 project 3: a menu-driven calculator (topics 1-3).

The first project that uses topic 3, control flow and functions, so the program can
finally make decisions, repeat itself and be split into functions:
- Functions: one job per function, parameters, return, returning two values
- if / elif / else: picking the operation, and catching bad input before it causes an error
- while loops: the menu, and asking again until the input is valid
- for loops: checking a number character by character, printing the history
- String formatting: str.format() and the format spec mini-language
- Dicts: the table of supported operators

It only uses what was covered up to session 05, so there is no try / except
(that's session 06). Every input is checked with if before it's used.

Run it with:
    python Assignment/s05-python-2-hash/project-3/calculator.py
"""

import math

OPERATORS = {
    "+": "add",
    "-": "subtract",
    "*": "multiply",
    "/": "divide",
    "//": "floor divide",
    "%": "remainder",
    "**": "power",
}

# Floats overflow just above 1.79e308, so results are kept below 1e308
LIMIT = 1e308
LIMIT_DIGITS = 308


def is_number(text):
    """Return True if text is a plain number such as 42, -3.5 or .5."""
    text = text.strip()
    if text.startswith(("+", "-")):
        text = text[1:]
    if text.count(".") > 1:
        return False
    digits = text.replace(".", "")
    if digits == "":  # "", "+" or "." on its own
        return False
    for char in digits:
        if char not in "0123456789":
            return False
    return True


def read_number(text, previous=None):
    """Turn the user's text into a float. "ans" means the previous result.

    Returns two values, (number, error). When the text isn't valid, number is
    None and error says why.
    """
    text = text.strip().lower()
    if text == "ans":
        if previous is None:
            return None, "there is no previous answer yet"
        return previous, None
    if not is_number(text):
        return None, "'{}' is not a number".format(text)
    number = float(text)  # safe: is_number() already checked the text
    if abs(number) > LIMIT:
        return None, "numbers above 1e308 are too large"
    return number, None


def calculate(a, operator, b):
    """Work out a <operator> b.

    Returns two values, (result, error). When the calculation isn't possible,
    result is None and error says why, so the caller never has to deal with a crash.
    """
    if operator not in OPERATORS:
        return None, "unknown operator '{}'".format(operator)
    if operator in ("/", "//", "%") and b == 0:
        return None, "cannot divide by zero"
    if operator == "**":
        if a == 0 and b < 0:
            return None, "0 cannot be raised to a negative power"
        if a < 0 and b != int(b):
            return None, "a negative number to a fractional power is not a real number"
        # a ** b has about b * log10(|a|) digits; checking first avoids an OverflowError
        if a != 0 and b * math.log10(abs(a)) > LIMIT_DIGITS:
            return None, "result is too large"

    if operator == "+":
        result = a + b
    elif operator == "-":
        result = a - b
    elif operator == "*":
        result = a * b
    elif operator == "/":
        result = a / b
    elif operator == "//":
        result = a // b
    elif operator == "%":
        result = a % b
    else:  # "**"
        result = a ** b

    if abs(result) > LIMIT:  # also catches inf, e.g. 1e300 * 1e300
        return None, "result is too large"
    return result, None


def format_number(value):
    """Return value as neat text: 2 not 2.0, 1,234.5 not 1234.5, at most 10 significant digits."""
    if value == 0:
        value = 0.0  # so -0.0 (e.g. from -1 * 0) prints as 0, not -0
    return "{:,.10g}".format(value)


def format_calculation(a, operator, b, result):
    """Return one line of history, e.g. '1,250 * 3 = 3,750'."""
    return "{} {} {} = {}".format(format_number(a), operator, format_number(b), format_number(result))


def ask_number(prompt, previous):
    """Keep asking until the user types a valid number (or "ans")."""
    while True:
        number, error = read_number(input(prompt), previous)
        if error is None:
            return number
        print("  " + error + ", try again")


def ask_operator():
    """Keep asking until the user types one of the supported operators."""
    prompt = "Operator ({}): ".format(" ".join(OPERATORS))
    while True:
        operator = input(prompt).strip()
        if operator in OPERATORS:
            return operator
        print("  '{}' is not an operator, try again".format(operator))


def show_history(history):
    if not history:
        print("  No calculations yet.")
        return
    number = 1
    for line in history:
        print("{:>3}. {}".format(number, line))
        number += 1


MENU = """
1. New calculation
2. Show history
3. Clear history
4. Quit"""


def main():
    history = []
    previous = None  # the last result, used when the user types "ans"
    print("{:=^34}".format(" CALCULATOR "))

    while True:
        print(MENU)
        choice = input("Choose 1-4: ").strip()

        if choice == "1":
            a = ask_number("First number (or ans): ", previous)
            operator = ask_operator()
            b = ask_number("Second number (or ans): ", previous)
            result, error = calculate(a, operator, b)
            if error is None:
                line = format_calculation(a, operator, b, result)
                history.append(line)
                previous = result
                print("  " + line)
            else:
                print("  Error: " + error)

        elif choice == "2":
            show_history(history)

        elif choice == "3":
            history.clear()
            print("  History cleared.")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Please enter a number from 1 to 4.")


if __name__ == "__main__":
    main()
