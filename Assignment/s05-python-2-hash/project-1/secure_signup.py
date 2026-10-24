"""Session 05 project 1: secure sign-up and log-in (topic 1: hash).

Uses ONLY topic 1 of the session, hashing, on top of the basics from sessions 04-05:
variables, data types, operators, strings, lists, sets, dicts, input() and print().

- A password is never stored: a random salt and a slow, salted hash are stored instead
- The users are kept in a dict, which is a hash table: finding a user is one lookup
- Logging in hashes the attempt with the same salt and compares the two hashes
- hash(), buckets, and `in` on a dict and a set, to see the hash table at work

There's no if / else, no loops, no functions of your own and no f-strings yet: string
formatting is topic 2 (project 2), and control flow and functions are topic 3
(projects 3-5). So the program runs straight from top to bottom, and a dict lookup
stands in where an if would normally go.

Run it with:
    python Assignment/s05-python-2-hash/project-1/secure_signup.py
"""

import hashlib
import os

ITERATIONS = 100_000  # slow on purpose, so guessing passwords from a leaked hash takes ages
LINE = "=" * 50

print(LINE)
print("STEP 1: SIGN UP")
print(LINE)
username = input("Choose a username: ").strip().lower()  # usernames ignore case and spaces
password = input("Choose a password: ")

salt = os.urandom(16)  # 16 random bytes, different for every user
password_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERATIONS)

users = {}  # username -> record. A dict is a hash table.
users[username] = {"salt": salt.hex(), "hash": password_hash.hex()}  # .hex() turns bytes into readable text

print()
print("Saved record for", username + ":")
print(users[username])
print("Fields stored:", list(users[username]))  # no "password" field: it's never kept
print("Password length:", len(password), "characters")
print("Hash length:    ", len(password_hash.hex()), "hex characters (the same for every password)")

print()
print(LINE)
print("STEP 2: LOG IN")
print(LINE)
login_username = input("Username: ").strip().lower()
login_password = input("Password: ")

# Look the user up in the hash table. An unknown username gets an empty record, so the
# hashes below just don't match: no if is needed, and the message is the same either way,
# so nobody can find out which usernames exist.
record = users.get(login_username, {"salt": "", "hash": ""})
attempt_hash = hashlib.pbkdf2_hmac("sha256", login_password.encode(), bytes.fromhex(record["salt"]), ITERATIONS)
login_ok = attempt_hash.hex() == record["hash"]

# A dict can stand in for if / else: True and False are keys like any other
messages = {True: "Login successful. Welcome, " + login_username + "!", False: "Invalid username or password."}
print(messages[login_ok])

print()
print(LINE)
print("STEP 3: WHY THE SALT MATTERS")
print(LINE)
same_salt_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERATIONS)
new_salt_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), os.urandom(16), ITERATIONS)
print("Same password, same salt -> same hash?", same_salt_hash == password_hash)
print("Same password, new salt  -> same hash?", new_salt_hash == password_hash)
print("So two users with the same password still get different hashes.")
print("Without a salt, EVERYONE with your password has this SHA-256:")
print(hashlib.sha256(password.encode()).hexdigest())
print("which is why leaked unsalted hashes are easy to look up and crack.")

print()
print(LINE)
print("STEP 4: INSIDE THE HASH TABLE")
print(LINE)
print("hash('" + username + "') =", hash(username))
print("In a table of 8 buckets it goes in bucket", hash(username) % 8)
print("(String hashes change every run: start the program again and compare.)")
print("'" + username + "' in users:", username in users)  # one lookup, however many users
print("'nobody' in users:", "nobody" in users)
reserved = {"admin", "root", "support"}  # a set is a hash table too
print("Is '" + username + "' a reserved name?", username in reserved)
