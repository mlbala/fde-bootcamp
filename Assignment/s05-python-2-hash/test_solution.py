import pytest

from solution import HashTable


@pytest.fixture
def table():
    t = HashTable()
    t.set("asha", 92)
    t.set("ravi", 45)
    t.set("monal", 78)
    return t


def test_get_returns_stored_values(table):
    assert table.get("asha") == 92
    assert table.get("ravi") == 45
    assert table.get("monal") == 78
    assert len(table) == 3


def test_set_existing_key_updates_without_adding(table):
    table.set("asha", 99)
    assert table.get("asha") == 99
    assert len(table) == 3


def test_get_missing_key_raises_key_error(table):
    with pytest.raises(KeyError):
        table.get("alex")


def test_delete_removes_key(table):
    table.delete("ravi")
    assert "ravi" not in table
    assert len(table) == 2
    with pytest.raises(KeyError):
        table.get("ravi")


def test_delete_missing_key_raises_key_error(table):
    with pytest.raises(KeyError):
        table.delete("alex")


def test_contains(table):
    assert "monal" in table
    assert "alex" not in table


def test_square_bracket_syntax():
    t = HashTable()
    t["x"] = 1
    assert t["x"] == 1
    del t["x"]
    assert len(t) == 0


def test_items_and_keys(table):
    assert sorted(table.items()) == [("asha", 92), ("monal", 78), ("ravi", 45)]
    assert sorted(table.keys()) == ["asha", "monal", "ravi"]


def test_colliding_keys_share_a_bucket_and_stay_retrievable():
    # hash(n) == n for small ints, so 1, 9 and 17 all land in bucket 1 of 8
    t = HashTable(capacity=8, max_load_factor=10)
    for n in (1, 9, 17):
        t.set(n, f"value {n}")
    assert t.bucket_index(1) == t.bucket_index(9) == t.bucket_index(17) == 1
    assert [t.get(n) for n in (1, 9, 17)] == ["value 1", "value 9", "value 17"]
    t.delete(9)
    assert t.get(1) == "value 1"
    assert t.get(17) == "value 17"


def test_resizes_when_load_factor_is_exceeded():
    t = HashTable(capacity=4)
    for n in range(3):
        t.set(n, n)
    assert t.capacity == 4  # 3 / 4 = 0.75 is not above the limit yet
    t.set(3, 3)
    assert t.capacity == 8  # 4 / 4 = 1.0 > 0.75, so the buckets doubled
    assert t.load_factor == 0.5
    assert [t.get(n) for n in range(4)] == [0, 1, 2, 3]


def test_mixed_hashable_key_types():
    t = HashTable()
    keys = [42, "42", 4.2, (4, 2), None, frozenset({4, 2})]
    for key in keys:
        t.set(key, repr(key))
    assert [t.get(key) for key in keys] == [repr(key) for key in keys]


def test_equal_keys_are_one_key_like_dict():
    # 1 == 1.0 == True and they hash the same, so a dict treats them as one key
    t = HashTable()
    t.set(1, "int")
    t.set(1.0, "float")
    t.set(True, "bool")
    expected = {1: "int", 1.0: "float", True: "bool"}
    assert len(t) == len(expected) == 1
    assert t.items() == list(expected.items())
    assert type(t.keys()[0]) is int  # the first key object is kept, as in dict


def test_unhashable_key_raises_type_error():
    t = HashTable()
    with pytest.raises(TypeError):
        t.set([1, 2], "list")


@pytest.mark.parametrize("capacity", [0, -1])
def test_invalid_capacity_raises(capacity):
    with pytest.raises(ValueError):
        HashTable(capacity=capacity)


def test_invalid_load_factor_raises():
    with pytest.raises(ValueError):
        HashTable(max_load_factor=0)


def test_matches_dict_after_many_operations():
    t, d = HashTable(capacity=1), {}
    for n in range(500):
        t.set(f"key{n}", n)
        d[f"key{n}"] = n
    for n in range(0, 500, 3):
        t.delete(f"key{n}")
        del d[f"key{n}"]
    for n in range(0, 500, 5):
        t.set(f"key{n}", -n)
        d[f"key{n}"] = -n
    assert len(t) == len(d)
    assert sorted(t.items()) == sorted(d.items())
    assert t.load_factor <= t.max_load_factor


def test_show_prints_every_bucket(capsys):
    t = HashTable(capacity=2)
    t.set(1, "one")
    t.show()
    assert capsys.readouterr().out == "bucket 0: []\nbucket 1: [(1, 'one')]\n"


def test_repr():
    t = HashTable(capacity=8)
    t.set("a", 1)
    assert repr(t) == "HashTable({'a': 1}, capacity=8)"
