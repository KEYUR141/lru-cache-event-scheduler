"""Meeting attendance and room counts for half-open intervals [start, end)."""

import heapq


def _sorted_events(events):
    """Validate comparable time pairs and sort a copy by start time."""
    copied_events = list(events)
    for start, end in copied_events:
        if start >= end:
            raise ValueError("Each event must have start < end")
    return sorted(copied_events)


def can_attend_all(events):
    """Return True if one person can attend every event without overlap."""
    sorted_events = _sorted_events(events)
    for index in range(1, len(sorted_events)):
        previous_end = sorted_events[index - 1][1]
        current_start = sorted_events[index][0]
        if current_start < previous_end:
            return False
    return True


def min_rooms_required(events):
    """Return peak simultaneous meetings, allowing adjacent room reuse."""
    sorted_events = _sorted_events(events)
    active_end_times = []
    max_rooms = 0

    for start, end in sorted_events:
        # End times equal to start also release their rooms.
        while active_end_times and active_end_times[0] <= start:
            heapq.heappop(active_end_times)
        heapq.heappush(active_end_times, end)
        max_rooms = max(max_rooms, len(active_end_times))

    return max_rooms


if __name__ == "__main__":
    events = [(9, 12), (10, 11), (11, 13)]
    print(can_attend_all(events))      # False
    print(min_rooms_required(events))  # 2
