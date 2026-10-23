# LRU Cache and Event Scheduler

Python solutions to Avaloka's Data Structures and Systems Design assignment by Keyur Sherke.

- **Problem 1:** A fixed-capacity LRU cache using a dictionary and a custom doubly linked list. `get` and `put` take average O(1) time.
- **Problem 2:** Meeting attendance detection and minimum room calculation using sorting and a min-heap.

The [submission PDF](docs/Keyur_Sherke_Avaloka_Assignment.pdf) includes the approach before each implementation and all four discussion answers. The [analysis](docs/analysis.md) is also available as readable Markdown.

## Run

Requires Python 3.10 or newer. The solutions and tests use only the standard library; no installation or API keys are needed.

From the repository root:

```bash
python lru_cache.py
python event_scheduler.py
python -m unittest discover -s tests -v
```

Expected demo output:

```text
# lru_cache.py
10
-1
A  <------>  C

# event_scheduler.py
False
2
```

## Files

```text
.
|-- lru_cache.py
|-- event_scheduler.py
|-- tests/
|   |-- test_lru_cache.py
|   `-- test_event_scheduler.py
`-- docs/
    |-- analysis.md
    `-- Keyur_Sherke_Avaloka_Assignment.pdf
```

## Usage

```python
from lru_cache import LRUCache
from event_scheduler import can_attend_all, min_rooms_required

cache = LRUCache(2)
cache.put("A", 10)
cache.put("B", 20)
assert cache.get("A") == 10
cache.put("C", 30)
assert cache.get("B") == -1

events = [(9, 12), (10, 11), (11, 13)]
assert can_attend_all(events) is False
assert min_rooms_required(events) == 2
```

## Behavior and assumptions

- Cache capacity must be a nonnegative integer. Negative capacity raises `ValueError`; other types, including booleans, raise `TypeError`. A zero-capacity cache stores nothing.
- Cache keys must be hashable; integer values are intended. A missing key returns `-1`. Successful reads and updates both refresh recency. A stored value of `-1` is indistinguishable from a miss by return value alone, as specified by the assignment.
- `display()` prints keys from least to most recent without changing recency. It is an O(n) debugging helper and is not called by `get` or `put`.
- Events are pairs of mutually comparable, finite time values with `start < end`. Zero-duration and reversed intervals raise `ValueError`. Times must use a common unit. Negative times are allowed; clock or date parsing is outside this interface.
- Intervals are half-open: a meeting ending at a time can share its room with one starting then. Duplicate events count as separate meetings.
- Neither scheduler function mutates the input. Empty input returns `True` for attendance and `0` rooms.
- The cache is single-threaded. Locking requirements and room assignment extensions are explained in the analysis.

## Verification

The 13 unit tests include eviction order, updates at capacity, zero and one capacity, invalid capacities, display behavior, later overlaps, adjacency, nested and duplicate events, peak occupancy before the final event, invalid intervals, and input preservation.

A fixed random seed makes additional comparisons reproducible: 1,000 cache operations are checked against `OrderedDict`, including linked-list invariants, and 200 schedules are checked against pairwise-overlap and direct-occupancy oracles.
