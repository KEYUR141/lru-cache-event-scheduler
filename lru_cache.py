class _Node:
    def __init__(self,key=None,value=None):
        self.key = key
        self.value = value
        self.next = None
        self.prev= None


class LRUCACHE:
    def __init__(self,capacity:int):
        if capacity < 0:
            raise ValueError("Capacity cannot be negative")

        self.capacity = capacity
        self.nodes = {}

        self.head = _Node()
        self.tail = _Node()

        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self,node:_Node) -> None:

        previous_node = node.prev
        next_node = node.next

        previous_node.next = next_node
        next_node.prev = previous_node

        node.prev = None
        node.next = None

    def _add_to_most_recent(self, node: _Node)->None:
        previous_node = self.tail.prev

        previous_node.next = node
        node.prev = previous_node
        node.next = self.tail
        self.tail.prev = node

    def get(self,key:int) -> int:
        if key not in self.nodes:
            return -1


        node = self.nodes[key]

        self._remove(node)
        self._add_to_most_recent(node)

        return node.value

    def put(self, key:int, value:int) -> None:

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

        node = _Node(key,value)
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

if __name__ == '__main__':
    
    cache= LRUCACHE(5)
    cache.put("A",1)
    cache.put("B",2)
    cache.put("C",3)

    cache.get("A")
    cache.display()
    #cache._add_to_most_recent("B")

    print(cache.get("A"))



