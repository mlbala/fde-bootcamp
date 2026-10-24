"""Session 05 project 4: a user login system that stores hashed passwords (topics 1-3).

Project 1 grown up: now that topic 3 is here, it has a menu, password rules and
account locking. Brings all of the session's topics together:
- Hashing: a salted, slow hash with hashlib.pbkdf2_hmac, never the password itself
- Hash tables: the users are kept in a dict, so finding one is a single O(1) lookup
- Nested dicts: each user's record holds their salt, hash and failed login count
- if / elif / else, while and for loops, and functions that return values
- String formatting: the aligned user table

It only uses what was covered up to session 05: no try / except, classes or files.
The users live in memory, so they are gone when the program stops.

Run it with:
    python Assignment/s05-python-2-hash/project-4/login_system.py
"""

import getpass
import hashlib
import hmac
import os

ITERATIONS = 100_000  # slow on purpose, so guessing passwords from a leaked hash takes ages
MAX_ATTEMPTS = 3
SYMBOLS = "!@#$%^&*()-_=+[]{};:'\",.<>/?\\|`~"
USERNAME_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789_"
LOGIN_FAILED = "invalid username or password"  # same message either way: don't reveal which usernames exist


def hash_password(password, salt=None):
    """Return (salt, hash) for password. A new random salt is made unless one is given."""
    if salt is None:
        salt = os.urandom(16)  # 16 random bytes, different for every user
    password_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERATIONS)
    return salt, password_hash


def password_matches(record, password):
    """Hash the attempt with the user's own salt and compare it with the stored hash."""
    _, attempt_hash = hash_password(password, record["salt"])
    # compare_digest takes the same time whether the first or the last byte differs
    return hmac.compare_digest(attempt_hash, record["hash"])


def username_problem(username, users):
    """Return what's wrong with a new username, or None if it's fine."""
    if len(username) < 3 or len(username) > 15:
        return "username must be 3 to 15 characters"
    for char in username:
        if char not in USERNAME_CHARS:
            return "username can only contain letters, digits and _"
    if username in users:  # one hash lookup, however many users there are
        return "username '{}' is already taken".format(username)
    return None


def password_problems(password):
    """Return a list of every rule the password breaks. An empty list means it's strong."""
    has_upper = has_lower = has_digit = has_symbol = False
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in SYMBOLS:
            has_symbol = True

    problems = []
    if len(password) < 8:
        problems.append("needs at least 8 characters")
    if not has_upper:
        problems.append("needs an upper case letter")
    if not has_lower:
        problems.append("needs a lower case letter")
    if not has_digit:
        problems.append("needs a digit")
    if not has_symbol:
        problems.append("needs a symbol such as ! @ # $")
    return problems


def clean_username(username):
    """Usernames are case-insensitive, so "Bala " and "bala" are the same user."""
    return username.strip().lower()


def register(users, username, password):
    """Add a new user. Returns an error message, or None if the account was created."""
    username = clean_username(username)
    problem = username_problem(username, users)
    if problem is not None:
        return problem
    if password_problems(password):
        return "password is too weak"
    salt, password_hash = hash_password(password)
    users[username] = {"salt": salt, "hash": password_hash, "failed": 0}
    return None


def is_locked(record):
    return record["failed"] >= MAX_ATTEMPTS


def login(users, username, password):
    """Check one login attempt. Returns two values: (True or False, message)."""
    record = users.get(clean_username(username))  # .get() gives None for an unknown user
    if record is None:
        return False, LOGIN_FAILED
    if is_locked(record):
        return False, "account is locked after {} failed logins".format(MAX_ATTEMPTS)
    if password_matches(record, password):
        record["failed"] = 0
        return True, "welcome, {}!".format(clean_username(username))

    record["failed"] += 1
    if is_locked(record):
        return False, "wrong password: account is now locked"
    return False, LOGIN_FAILED


def change_password(users, username, old_password, new_password):
    """Replace a user's password. Returns an error message, or None if it was changed."""
    ok, message = login(users, username, old_password)
    if not ok:
        return message
    if new_password == old_password:
        return "the new password must be different from the old one"
    if password_problems(new_password):
        return "new password is too weak"
    salt, password_hash = hash_password(new_password)  # a new password gets a new salt too
    users[clean_username(username)].update({"salt": salt, "hash": password_hash})
    return None


def format_users(users):
    """Return the user table as text. It shows only the start of each salt and hash."""
    if not users:
        return "No users yet."
    lines = ["{:<16} {:<14} {:<14} {:>6}  {}".format("Username", "Salt", "Hash", "Failed", "Status")]
    for username, record in users.items():  # in the order they signed up
        status = "locked" if is_locked(record) else "active"
        lines.append(
            "{:<16} {:<14} {:<14} {:>6}  {}".format(
                username, record["salt"].hex()[:12], record["hash"].hex()[:12], record["failed"], status
            )
        )
    return "\n".join(lines)


def ask_new_password(prompt):
    """Keep asking until the password passes every rule, listing what's wrong each time."""
    while True:
        password = getpass.getpass(prompt)
        problems = password_problems(password)
        if not problems:
            return password
        print("  Password is too weak:")
        for problem in problems:
            print("  - " + problem)


MENU = """
1. Register
2. Log in
3. Change password
4. List users
5. Quit"""


def main():
    users = {}  # username -> {"salt": bytes, "hash": bytes, "failed": int}
    print("{:=^40}".format(" LOGIN SYSTEM "))

    while True:
        print(MENU)
        choice = input("Choose 1-5: ").strip()

        if choice == "1":
            username = clean_username(input("Username: "))
            problem = username_problem(username, users)
            if problem is not None:
                print("  " + problem)
                continue
            password = ask_new_password("Password (typing is hidden): ")
            register(users, username, password)
            print("  Account '{}' created.".format(username))

        elif choice == "2":
            username = input("Username: ")
            attempts = 0
            while attempts < MAX_ATTEMPTS:
                ok, message = login(users, username, getpass.getpass("Password: "))
                print("  " + message)
                if ok or "locked" in message:
                    break
                attempts += 1
                left = MAX_ATTEMPTS - attempts
                if left > 0:
                    print("  {} {} left".format(left, "try" if left == 1 else "tries"))

        elif choice == "3":
            username = input("Username: ")
            old_password = getpass.getpass("Current password: ")
            new_password = ask_new_password("New password: ")
            error = change_password(users, username, old_password, new_password)
            print("  " + (error if error is not None else "Password changed."))

        elif choice == "4":
            print(format_users(users))

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
