"""Session 06 project 1: an ATM machine (topic 1: exception handling).

Uses topic 1 of the session, exception handling, on top of sessions 04-05
(functions, if / elif / else, loops, dicts, string formatting):
- try / except, catching a specific exception: ValueError from float(), KeyError from a dict
- else, which runs only when nothing went wrong, and finally, which always runs
- raise, with custom exceptions for the bank's own rules
- how an exception travels up from the function that raised it to the menu that catches it
- one base class, ATMError, so a single except catches every bank error

It doesn't use os, files, OOP, comprehensions, lambda or the session's built-ins yet:
those are topics 2-7, practised in projects 2-4. So the accounts live in a dict in
memory and start fresh every run. The custom exceptions are one-line classes, written
the way 01_exception_handling.ipynb writes them; real classes come in project 3.

Run it with:
    python Assignment/s06-python-3/project-1/atm.py
Try account 1001 with PIN 1234, or account 1002 with PIN 4321.
"""

import math

MAX_PIN_TRIES = 3
NOTE = 100  # the smallest note in the machine, so withdrawals must be a multiple of it
DAILY_LIMIT = 20_000
MAX_DEPOSIT = 50_000
STATEMENT_SIZE = 5


class ATMError(Exception):
    """Base class for every ATM error: `except ATMError` catches all of them."""


class AccountNotFoundError(ATMError):
    """No account has that number."""


class WrongPinError(ATMError):
    """The PIN doesn't match."""


class CardBlockedError(ATMError):
    """Too many wrong PINs, so the card is blocked."""


class InvalidAmountError(ATMError):
    """The amount isn't a positive number, or isn't one the machine can pay out."""


class InsufficientFundsError(ATMError):
    """The balance is too low for this withdrawal."""


class DailyLimitError(ATMError):
    """This withdrawal would go over the daily limit."""


class InvalidPinError(ATMError):
    """A new PIN that isn't 4 digits, or doesn't match when typed again."""


def new_accounts():
    """Return the bank's accounts. A function, so every run (and every test) starts fresh.

    A real bank never stores the PIN itself, only a salted hash of it (see session 05,
    projects 1 and 4). It's kept as plain text here so the project stays about exceptions.
    """
    return {
        "1001": {"name": "Bala", "pin": "1234", "balance": 15_000.0, "withdrawn_today": 0.0,
                 "wrong_pins": 0, "blocked": False, "history": []},
        "1002": {"name": "Kumar", "pin": "4321", "balance": 2_500.0, "withdrawn_today": 0.0,
                 "wrong_pins": 0, "blocked": False, "history": []},
    }


def find_account(accounts, number):
    """Return the account with this number. Raises AccountNotFoundError if there isn't one."""
    number = number.strip()
    try:
        return accounts[number]
    except KeyError:
        # Turn the dict's KeyError into an error that explains the problem.
        # "from None" hides the KeyError, so the traceback only shows ours.
        raise AccountNotFoundError(f"no account with number '{number}'") from None


def check_pin(account, pin):
    """Accept the PIN, or raise WrongPinError, or CardBlockedError after too many wrong PINs."""
    if account["blocked"]:
        raise CardBlockedError("this card is blocked, please contact your branch")
    if pin.strip() != account["pin"]:
        account["wrong_pins"] += 1
        tries_left = MAX_PIN_TRIES - account["wrong_pins"]
        if tries_left == 0:
            account["blocked"] = True
            raise CardBlockedError(f"wrong PIN {MAX_PIN_TRIES} times, so the card is now blocked")
        raise WrongPinError(f"wrong PIN, {tries_left} {'try' if tries_left == 1 else 'tries'} left")
    account["wrong_pins"] = 0


def parse_amount(text):
    """Turn the user's text into an amount. Raises InvalidAmountError if it isn't a valid one."""
    try:
        amount = float(text.replace(",", ""))  # "1,500" is fine too
    except ValueError:
        raise InvalidAmountError(f"'{text.strip()}' is not an amount") from None
    if not math.isfinite(amount) or amount <= 0:  # float() also accepts "nan" and "inf"
        raise InvalidAmountError("the amount must be a positive number")
    if round(amount, 2) != amount:
        raise InvalidAmountError("an amount can't have more than 2 decimal places")
    return amount


def add_to_history(account, kind, change):
    account["history"].append({"type": kind, "change": change, "balance": account["balance"]})


def deposit(account, amount):
    if amount > MAX_DEPOSIT:
        raise InvalidAmountError(f"at most Rs {MAX_DEPOSIT:,} per deposit")
    account["balance"] += amount
    add_to_history(account, "Deposit", amount)


def withdraw(account, amount):
    """Take money out. Raises an ATMError if the machine or the bank won't allow it."""
    if amount % NOTE != 0:
        raise InvalidAmountError(f"the machine only has Rs {NOTE} notes, so enter a multiple of {NOTE}")
    if amount > account["balance"]:
        raise InsufficientFundsError(f"your balance is only Rs {account['balance']:,.2f}")
    if account["withdrawn_today"] + amount > DAILY_LIMIT:
        left = DAILY_LIMIT - account["withdrawn_today"]
        raise DailyLimitError(f"the daily limit is Rs {DAILY_LIMIT:,}, you can take Rs {left:,.0f} more today")
    account["balance"] -= amount
    account["withdrawn_today"] += amount
    add_to_history(account, "Withdraw", -amount)


def change_pin(account, old_pin, new_pin, new_pin_again):
    check_pin(account, old_pin)  # a wrong PIN raises here, and the exception travels up to the menu
    new_pin = new_pin.strip()
    if len(new_pin) != 4 or not new_pin.isdecimal():
        raise InvalidPinError("the new PIN must be exactly 4 digits")
    if new_pin != new_pin_again.strip():
        raise InvalidPinError("the two new PINs don't match")
    if new_pin == account["pin"]:
        raise InvalidPinError("the new PIN must be different from the old one")
    account["pin"] = new_pin


def format_statement(account):
    """Return the last few transactions and the balance as text."""
    lines = [f"Mini statement for {account['name']}", f"{'Type':<10}{'Amount':>12}{'Balance':>14}"]
    recent = account["history"][-STATEMENT_SIZE:]  # slicing: the last 5, or fewer
    if not recent:
        lines.append("No transactions yet.")
    for entry in recent:
        lines.append(f"{entry['type']:<10}{entry['change']:>+12,.2f}{entry['balance']:>14,.2f}")
    lines.append(f"{'Balance':<10}{account['balance']:>26,.2f}")
    return "\n".join(lines)


def log_in(accounts):
    """Ask for the account number and PIN. Returns the account, or None if it can't be used."""
    try:
        account = find_account(accounts, input("Account number: "))
    except AccountNotFoundError as e:
        print("  Error:", e)
        return None

    while True:
        try:
            check_pin(account, input("PIN: "))
        except WrongPinError as e:
            print(" ", e)  # not fatal: ask again
        except CardBlockedError as e:
            print("  Error:", e)
            return None
        else:  # runs only if check_pin() raised nothing
            print(f"  Welcome, {account['name']}!")
            return account


MENU = """
1. Check balance
2. Deposit
3. Withdraw
4. Mini statement
5. Change PIN
6. Take card"""


def serve(account):
    """The menu for one customer, until they take their card."""
    while True:
        print(MENU)
        choice = input("Choose 1-6: ").strip()
        try:
            if choice == "1":
                print(f"  Balance: Rs {account['balance']:,.2f}")

            elif choice == "2":
                amount = parse_amount(input("Amount to deposit: "))
                deposit(account, amount)
                print(f"  Deposited Rs {amount:,.2f}. Balance: Rs {account['balance']:,.2f}")

            elif choice == "3":
                amount = parse_amount(input("Amount to withdraw: "))
                withdraw(account, amount)
                print(f"  Please take your cash: Rs {amount:,.0f}. Balance: Rs {account['balance']:,.2f}")

            elif choice == "4":
                print(format_statement(account))

            elif choice == "5":
                change_pin(account, input("Current PIN: "), input("New PIN: "), input("New PIN again: "))
                print("  PIN changed.")

            elif choice == "6":
                return

            else:
                print("Please enter a number from 1 to 6.")

        # The more specific exception has to come first: CardBlockedError is also an ATMError
        except CardBlockedError as e:
            print("  Error:", e)
            return  # a blocked card is kept, so the session ends
        except ATMError as e:  # every other bank error: explain it and show the menu again
            print("  Error:", e)


def main():
    accounts = new_accounts()
    print("Welcome to FDE Bank. Try account 1001 (PIN 1234) or 1002 (PIN 4321).")
    while True:
        print()
        if input("Insert card? (y/n): ").strip().lower() != "y":
            break
        try:
            account = log_in(accounts)
            if account is not None:
                serve(account)
        finally:
            # Runs however the session ends, even on Ctrl + C, so no card is left in the machine
            print("  Please take your card.")
    print("ATM switched off.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):  # Ctrl + C or Ctrl + D
        print("\nATM switched off.")
