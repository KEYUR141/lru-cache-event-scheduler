import io
import random
import unittest
from collections import OrderedDict
from contextlib import redirect_stdout

from lru_cache import LRUCache


class LRUCacheTests(unittest.TestCase):
    def test_access_changes_eviction_order(self):
        cache = LRUCache(2)
        cache.put("A", 10)
        cache.put("B", 20)
        self.assertEqual(cache.get("A"), 10)
        cache.put("C", 30)
        self.assertEqual(cache.get("B"), -1)
        self.assertEqual(cache.get("A"), 10)
        self.assertEqual(cache.get("C"), 30)

    def test_update_at_capacity_does_not_evict(self):
        cache = LRUCache(2)
        cache.put(1, 10)
        cache.put(2, 20)
        cache.put(1, 99)
        self.assertEqual(len(cache.nodes), 2)
        cache.put(3, 30)
        self.assertEqual(cache.get(2), -1)
        self.assertEqual(cache.get(1), 99)

    def test_missing_access_does_not_change_order(self):
        cache = LRUCache(2)
        cache.put(1, 10)
        cache.put(2, 20)
        self.assertEqual(cache.get(9), -1)
        cache.put(3, 30)
        self.assertEqual(cache.get(1), -1)
        self.assertEqual(cache.get(2), 20)

    def test_zero_capacity(self):
        cache = LRUCache(0)
        cache.put(1, 10)
        self.assertEqual(cache.get(1), -1)
        self.assertEqual(len(cache.nodes), 0)

    def test_capacity_one(self):
        cache = LRUCache(1)
        cache.put(1, 10)
        cache.put(1, 11)
        self.assertEqual(cache.get(1), 11)
        cache.put(2, 20)
        self.assertEqual(cache.get(1), -1)
        self.assertEqual(cache.get(2), 20)

    def test_invalid_capacity(self):
        with self.assertRaises(ValueError):
            LRUCache(-1)
        for capacity in (1.5, True, "2"):
            with self.subTest(capacity=capacity):
                with self.assertRaises(TypeError):
                    LRUCache(capacity)

    def test_display_preserves_order(self):
        cache = LRUCache(2)
        stream = io.StringIO()
        with redirect_stdout(stream):
            cache.display()
            cache.put("A", 10)
            cache.put("B", 20)
            cache.display()
        self.assertEqual(stream.getvalue(), "Cache is empty\nA  <------>  B\n")
        cache.put("C", 30)
        self.assertEqual(cache.get("A"), -1)

    def test_random_operations_against_ordered_dict(self):
        rng = random.Random(42)
        for capacity in range(5):
            cache = LRUCache(capacity)
            reference = OrderedDict()
            for _ in range(200):
                key = rng.randrange(8)
                if rng.choice((True, False)):
                    value = rng.randrange(-1, 100)
                    cache.put(key, value)
                    reference[key] = value
                    reference.move_to_end(key)
                    if len(reference) > capacity:
                        reference.popitem(last=False)
                else:
                    self.assertEqual(cache.get(key), reference.get(key, -1))
                    if key in reference:
                        reference.move_to_end(key)

                # Check bidirectional links, ordering, and map consistency.
                keys = []
                previous = cache.head
                current = cache.head.next
                while current is not cache.tail:
                    self.assertIs(current.prev, previous)
                    self.assertIs(cache.nodes[current.key], current)
                    keys.append(current.key)
                    self.assertLessEqual(len(keys), capacity)
                    previous, current = current, current.next
                self.assertIs(cache.tail.prev, previous)
                self.assertEqual(keys, list(reference))
                self.assertEqual(len(cache.nodes), len(reference))


if __name__ == "__main__":
    unittest.main()
