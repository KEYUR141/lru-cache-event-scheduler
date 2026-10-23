"""LRU cache: head.next is least recent; tail.prev is most recent.

get and put take average O(1) time. This class is not thread-safe.
"""

from collections.abc import Hashable


class _Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None


class LRUCache:
    """Cache integer values under hashable keys; a miss returns -1."""

    def __init__(self, capacity: int):
        if type(capacity) is not int:
            raise TypeError("Capacity must be an integer")
        if capacity < 0:
            raise ValueError("Capacity cannot be negative")

        self.capacity = capacity
        self.nodes = {}

        self.head = _Node()
        self.tail = _Node()

        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: _Node) -> None:
        previous_node = node.prev
        next_node = node.next

        previous_node.next = next_node
        next_node.prev = previous_node

        node.prev = None
        node.next = None

    def _add_to_most_recent(self, node: _Node) -> None:
        previous_node = self.tail.prev

        previous_node.next = node
        node.prev = previous_node
        node.next = self.tail
        self.tail.prev = node

    def get(self, key: Hashable) -> int:
        if key not in self.nodes:
            return -1

        node = self.nodes[key]

        self._remove(node)
        self._add_to_most_recent(node)

        return node.value

    def put(self, key: Hashable, value: int) -> None:
        if key in self.nodes:
            node = self.nodes[key]
            node.value = value

            self._remove(node)
            self._add_to_most_recent(node)
            return

        if self.capacity == 0:
            return

        if len(self.nodes) == self.capacity:
            least_recent = self.head.next

            self._remove(least_recent)
            del self.nodes[least_recent.key]

        node = _Node(key, value)
        self.nodes[key] = node
        self._add_to_most_recent(node)

    def display(self) -> None:
        current = self.head.next
        entries = []

        while current is not self.tail:
            entries.append(str(current.key))
            current = current.next

        if entries:
            print("  <------>  ".join(entries))
        else:
            print("Cache is empty")


if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put("A", 10)
    cache.put("B", 20)
    print(cache.get("A"))  # 10; A becomes most recent.
    cache.put("C", 30)    # Evicts B.
    print(cache.get("B"))  # -1
    cache.display()       # A  <------>  C
