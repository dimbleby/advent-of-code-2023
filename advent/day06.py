from __future__ import annotations

import math

from advent.utils import data_dir


def ways_to_beat(record: int, t: int) -> int:
    # x * (t - x) > record
    #
    # x^2 - tx + record < 0
    discriminant = t * t - 4 * record
    lo_root = (t - math.sqrt(discriminant)) / 2

    # We want the next integer.
    lo = int(lo_root) + 1
    hi = t - lo

    return hi - lo + 1


def solve() -> None:
    puzzle = data_dir() / "day06.txt"
    data = puzzle.read_text(encoding="utf-8").strip()
    lines = data.splitlines()
    times = [int(n) for n in lines[0].split()[1:]]
    distances = [int(n) for n in lines[1].split()[1:]]

    part_one = 1
    for d, t in zip(distances, times, strict=True):
        part_one *= ways_to_beat(d, t)
    print(f"Part one: {part_one}")

    big_time = int("".join(str(n) for n in times))
    big_distance = int("".join(str(n) for n in distances))
    part_two = ways_to_beat(big_distance, big_time)
    print(f"Part two: {part_two}")
