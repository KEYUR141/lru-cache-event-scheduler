import random
import unittest

from event_scheduler import can_attend_all, min_rooms_required


class EventSchedulerTests(unittest.TestCase):
    def test_examples_and_boundaries(self):
        cases = [
            ([], True, 0),
            ([(9, 10)], True, 1),
            ([(9, 10), (10, 11), (11, 12)], True, 1),
            ([(9, 12), (10, 11), (11, 13)], False, 2),
            ([(11, 12), (9, 10), (10, 11)], True, 1),
            ([(0, 10), (1, 9), (2, 8)], False, 3),
            ([(1, 3), (1, 3), (1, 3)], False, 3),
            ([(0, 2), (0, 2), (2, 3)], False, 2),
            ([(0, 2), (0, 3), (10, 11)], False, 2),
            ([(-3, -1), (-1, 0)], True, 1),
        ]
        for events, attendance, rooms in cases:
            with self.subTest(events=events):
                self.assertIs(can_attend_all(events), attendance)
                self.assertEqual(min_rooms_required(events), rooms)

    def test_overlap_after_first_pair(self):
        self.assertFalse(can_attend_all([(1, 2), (3, 5), (4, 6)]))

    def test_input_is_not_mutated(self):
        events = [(5, 8), (1, 3), (2, 4)]
        original = events.copy()
        can_attend_all(events)
        min_rooms_required(events)
        self.assertEqual(events, original)

    def test_invalid_intervals(self):
        for function in (can_attend_all, min_rooms_required):
            for events in ([(2, 2)], [(3, 1)]):
                with self.subTest(function=function.__name__, events=events):
                    with self.assertRaises(ValueError):
                        function(events)

    def test_random_inputs_against_independent_oracles(self):
        rng = random.Random(42)
        for _ in range(200):
            events = []
            for _ in range(rng.randrange(15)):
                start = rng.randrange(20)
                events.append((start, start + rng.randrange(1, 8)))
            no_overlap = all(
                end_a <= start_b or end_b <= start_a
                for i, (start_a, end_a) in enumerate(events)
                for start_b, end_b in events[i + 1:]
            )
            peak = max(
                (sum(start <= time < end for start, end in events)
                 for time, _ in events),
                default=0,
            )
            self.assertEqual(can_attend_all(events), no_overlap)
            self.assertEqual(min_rooms_required(events), peak)


if __name__ == "__main__":
    unittest.main()
