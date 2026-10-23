# Data Structures and Systems Design Assignment

Keyur Sherke | Avaloka | Python

This submission implements an LRU cache and an event scheduler. The explanations below describe the choices behind the code; the accompanying PDF contains both explanations and the complete implementations.

## Problem 1 approach

I need fast lookup as well as fast changes to usage order. I use a dictionary mapping each key to its node in a doubly linked list. The dictionary finds a node in average O(1) time, and its previous and next pointers let me detach and reposition it in O(1) time without searching the list.

The list runs from least recent to most recent. Two dummy sentinel nodes mark its ends: `head.next` is the least recent real entry and `tail.prev` is the most recent. Sentinels avoid separate insertion and removal cases for an empty list or a single entry.

For `get`, I return -1 for a missing key. Otherwise, I move its node to the most recent end and return the value. For `put`, I first handle existing keys by updating and moving their nodes. For a new key at capacity, I remove the least recent node from both structures, then insert the new entry at the most recent end. Each node stores its key so I can delete the dictionary entry during eviction without searching.

Every real node is represented exactly once in the dictionary and list. Lookup, update, insertion, and eviction preserve that invariant and keep the list in usage order. Thus the entry evicted from the head is always the least recently used.

With capacity 2, `put(A, 10)`, `put(B, 20)`, `get(A)`, `put(C, 30)` changes the order from A-B to B-A to A-C. B is evicted because accessing A refreshed its recency.

Capacity zero stores nothing. Negative capacity is invalid. The optional `display` helper traverses the list for learning and debugging, but neither cache operation calls it.

Implementation: [lru_cache.py](../lru_cache.py).

## Problem 2 approach

I interpret each meeting as a half-open interval [start, end). Equality between one end and another start is allowed. I validate `start < end`, then sort a copy by start time so the original input remains unchanged.

For `can_attend_all`, I compare each start with the previous meeting's end. If the start is smaller, those meetings overlap and I return False. If every adjacent pair passes, their chronological chain has no overlap, so I return True. Empty and single-event inputs also return True.

For `min_rooms_required`, I keep a min-heap of end times for active meetings. Before adding a meeting, I remove all end times less than or equal to its start; those meetings have released their rooms. I push the new end time and record the largest heap size seen. A heap exposes its smallest value at index zero, so I can repeatedly find the next meeting to finish without scanning all active meetings.

After each insertion, the heap contains exactly the meetings active at that start time. The peak heap size is necessary because simultaneous meetings need different rooms. It is sufficient because a room can be reused whenever its previous meeting finishes, and occupancy rises only when a meeting starts. Therefore the peak is the minimum number of rooms.

For [(9, 12), (10, 11), (11, 13)], the heaps after insertion are [12], [11, 12], and [12, 13]. The end time 11 is removed before the last insertion, so two rooms suffice. I return the maximum, not the final heap size, because the busiest moment may occur earlier.

Implementation: [event_scheduler.py](../event_scheduler.py).

## Final discussion and analysis

### 1 Time and space complexity

Let n be the number of events, c the configured cache capacity, and k the number of entries currently cached. Cache keys are assumed to have constant-cost hashing and equality, as with the small integer and string keys used here. Space below is auxiliary space unless stated otherwise.

| Function | Time | Space | Reason |
|---|---|---|---|
| `_Node.__init__` | O(1) | O(1) per node | Initializes four fields |
| `LRUCache.__init__` | O(1) | O(1) initially | Empty map and two sentinels; no preallocation |
| `_remove` | O(1) | O(1) | Fixed number of pointer changes |
| `_add_to_most_recent` | O(1) | O(1) | Fixed number of pointer changes |
| `get` | Average O(1) | O(1) | Dictionary lookup and list movement |
| `put` | Average amortized O(1) | O(1) per operation, excluding dictionary resize | At most one eviction and one insertion |
| `display` | O(k) | O(k) | Collects and joins printed key strings |
| `_sorted_events` | O(n log n) worst case | O(n) | Copies, validates, and sorts events |
| `can_attend_all` | O(n log n) worst case | O(n) | Sorting plus a linear adjacent scan |
| `min_rooms_required` | O(n log n) worst case | O(n) | Sorting and heap operations |

The cache as a whole uses O(k + 1) storage, bounded by O(c + 1), for the dictionary, data nodes, and two sentinels. Cache complexities assume bounded-size keys and values; display also depends on the total size of the strings printed. Dictionary resizing can make an individual insertion O(k), and pathological hash collisions can make dictionary operations O(k). The required O(1) cache performance is the conventional average/amortized guarantee of hash-map implementations.

In the scheduler, validation takes O(n). Python sorting and the copied lists require O(n) storage. The heap itself holds at most r end times, where r is peak occupancy and r <= n. Each meeting is pushed once and popped at most once across the entire loop, so the nested while loop does not make the algorithm quadratic. Total worst-case time is O(n log n) and auxiliary space is O(n).

### 2 LRU data structure trade-offs

A dictionary alone provides fast lookup but a plain key-value lookup interface does not express how to reposition and evict entries by recency. A doubly linked list alone maintains order but needs O(k) lookup. Combining them provides both operations efficiently, at the cost of a dictionary entry, a node, and two links per cached item, plus the responsibility of keeping both structures synchronized.

A Python list requires O(k) shifting when removing an arbitrary entry. A singly linked list cannot unlink a known node in O(1) without also knowing its predecessor. A timestamp heap makes recency updates or eviction O(log k), and lazy updates can accumulate stale entries. `collections.OrderedDict` offers a shorter practical implementation through `move_to_end` and `popitem(last=False)`; I implemented the linked list explicitly to demonstrate the required mechanics. Python's regular dictionaries preserve insertion order, but that alone does not automatically maintain access order.

### 3 Assigning specific rooms

I would sort `(start, end, original_index)` records and replace the end-time heap with a busy-room heap containing `(end, room_id)`. I would also maintain a min-heap of available room IDs and a counter for new IDs.

Before each meeting, I would pop every finished meeting from the busy heap and return its ID to the available heap. I would reuse the smallest available ID, or allocate a new ID if none is free, then push `(end, room_id)` into the busy heap. I would save the assignment at `assignments[original_index]` so unsorted and duplicate input events retain their individual identities. Integer IDs can be displayed as Room 1, Room 2, and so on, or mapped to Room A, Room B, and further labels.

For [(9, 12), (10, 11), (11, 13)], the assignments can be [Room A, Room B, Room B]. A new room is allocated only when all existing rooms are occupied, so this uses the minimum number of rooms. Time remains O(n log n), and auxiliary space remains O(n). This is a proposed extension, not an extra implemented API.

### 4 Making the cache thread-safe

I would create one `threading.Lock` for each cache instance and hold it for the entire body of every public `get` and `put`. A successful `get` modifies the linked list, so reads also require this lock. Lookup, movement, eviction, and dictionary insertion must form one atomic operation with respect to other callers; locking individual dictionary accesses is insufficient.

The private list helpers would assume their caller holds the lock. They would not acquire it again, avoiding nested acquisition of a non-reentrant lock. For `display`, I would copy the keys while holding the same lock, then release it before formatting and printing the snapshot. Any added public inspection method would also use that lock. Callers must not mutate internal nodes or the dictionary directly.

Python's GIL does not guarantee atomicity of these multi-step operations and is not a replacement for the cache lock. A single lock is simple and preserves a global LRU order, but serializes callers; waiting time under contention is not covered by the O(1) algorithmic bound. Sharding can improve throughput, but changes exact global LRU behavior unless extra coordination is added. This design addresses threads within one process; separate processes would need shared storage and process-safe coordination. The submitted cache itself is single-threaded.

## Verification

Run `python -m unittest discover -s tests -v` from the repository root. There are 13 tests, including 1,000 deterministic randomized cache operations checked against OrderedDict and 200 schedules checked against independent overlap and occupancy calculations. Tests also verify linked-list consistency and the boundary behaviors documented in the README.
