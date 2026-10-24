"""Session 05, assignment 1: a hash table built from scratch.

Shows what Python's dict and set do behind the scenes:
- hash(key) turns the key into an integer
- hash(key) % number_of_buckets picks the bucket the key belongs in
- keys that land in the same bucket (a collision) share it: each bucket is a
  list of (key, value) pairs, which is called "separate chaining"
- when the table gets too full, it doubles its number of buckets and moves
  every pair to its new bucket (resizing), so buckets stay short and fast

The step-by-step walkthrough is in understanding_hash.ipynb. Run the demo with:
    python Assignment/s05-python-2-hash/solution.py
"""


class HashTable:
    """A small dict-like hash table that handles collisions by chaining."""

    def __init__(self, capacity=8, max_load_factor=0.75):
        if capacity < 1:
            raise ValueError(f"capacity must be at least 1, got {capacity}")
        if max_load_factor <= 0:
            raise ValueError(f"max_load_factor must be positive, got {max_load_factor}")
        # One empty list per bucket ([[]] * capacity would share ONE list between all of them)
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0
        self.max_load_factor = max_load_factor

    @property
    def capacity(self):
        """Number of buckets."""
        return len(self._buckets)

    @property
    def load_factor(self):
        """How full the table is: number of items / number of buckets."""
        return self._size / self.capacity

    def bucket_index(self, key):
        """Return the index of the bucket that key belongs in."""
        # hash() raises TypeError for unhashable keys such as lists, just like dict does
        return hash(key) % self.capacity

    def set(self, key, value):
        """Store value under key, replacing the old value if key is already present."""
        bucket = self._buckets[self.bucket_index(key)]
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                # Same key: overwrite the value, keeping the original key object like dict does
                bucket[i] = (existing_key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self.load_factor > self.max_load_factor:
            self._resize(self.capacity * 2)

    def get(self, key):
        """Return the value stored under key. Raises KeyError if key is missing."""
        # Only the key's own bucket is searched, never the whole table
        for existing_key, value in self._buckets[self.bucket_index(key)]:
            if existing_key == key:
                return value
        raise KeyError(key)

    def delete(self, key):
        """Remove key and its value. Raises KeyError if key is missing."""
        bucket = self._buckets[self.bucket_index(key)]
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                del bucket[i]
                self._size -= 1
                return
        raise KeyError(key)

    def items(self):
        """Return every (key, value) pair as a list."""
        pairs = []
        for bucket in self._buckets:
            pairs.extend(bucket)
        return pairs

    def keys(self):
        """Return every key as a list."""
        return [key for key, _ in self.items()]

    def show(self):
        """Print each bucket and its contents, to see how the keys are spread out."""
        for index, bucket in enumerate(self._buckets):
            print(f"bucket {index}: {bucket}")

    def _resize(self, new_capacity):
        """Move every pair into a new, bigger list of buckets."""
        old_pairs = self.items()
        self._buckets = [[] for _ in range(new_capacity)]
        for key, value in old_pairs:
            # Re-hash: with more buckets, hash(key) % capacity gives a new index
            self._buckets[self.bucket_index(key)].append((key, value))

    # Special methods, so a HashTable works with Python's normal dict syntax
    def __len__(self):  # len(table)
        return self._size

    def __contains__(self, key):  # key in table
        try:
            self.get(key)
        except KeyError:
            return False
        return True

    def __getitem__(self, key):  # table[key]
        return self.get(key)

    def __setitem__(self, key, value):  # table[key] = value
        self.set(key, value)

    def __delitem__(self, key):  # del table[key]
        self.delete(key)

    def __repr__(self):  # what print(table) shows
        pairs = ", ".join(f"{key!r}: {value!r}" for key, value in self.items())
        return f"HashTable({{{pairs}}}, capacity={self.capacity})"


def main():
    table = HashTable(capacity=4)
    print("Empty table:", table)

    # 1. Insert: each key is hashed to pick its bucket.
    # String hashes are randomized per run, so these bucket numbers change each time.
    contacts = {"asha": "98450-11111", "ravi": "98450-22222", "monal": "98450-33333"}
    print("\n1. Insert")
    for name, phone in contacts.items():
        table.set(name, phone)
        print(f"  set {name!r:8} -> bucket {table.bucket_index(name)} "
              f"(size={len(table)}, capacity={table.capacity}, load={table.load_factor:.2f})")

    # 2. A 4th item makes the load factor 4 / 4 = 1.0 > 0.75, so the table doubles
    print("\n2. Resize")
    table["alex"] = "98450-44444"
    print(f"  after adding 'alex': capacity={table.capacity}, load={table.load_factor:.2f}")
    table.show()

    # 3. Look up, update, delete and test membership
    print("\n3. Lookup, update, delete")
    print("  ravi ->", table["ravi"])
    table["ravi"] = "98450-99999"
    print("  ravi after update ->", table["ravi"], f"(size is still {len(table)})")
    del table["asha"]
    print("  'asha' in table after delete:", "asha" in table)
    try:
        table.get("asha")
    except KeyError as error:
        print("  KeyError:", error)

    # 4. Collisions: small ints hash to themselves, so 1, 9 and 17 all land in bucket 1 of 8.
    # A high max_load_factor stops it resizing, so the chain stays visible.
    print("\n4. Collisions (chaining)")
    numbers = HashTable(capacity=8, max_load_factor=10)
    for n in (1, 9, 17, 4):
        numbers.set(n, f"value {n}")
    numbers.show()
    print("  get(17) ->", numbers.get(17))


if __name__ == "__main__":
    main()
