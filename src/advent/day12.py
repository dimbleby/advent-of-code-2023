from __future__ import annotations

import functools
from dataclasses import dataclass

from advent.utils import data_dir


@dataclass(frozen=True)
class Record:
    line: str
    pattern: tuple[int, ...]

    @staticmethod
    def from_string(text: str) -> Record:
        line, pattern = text.split()
        numbers = tuple(int(n) for n in pattern.split(","))
        return Record(line, numbers)


@functools.cache
def possibilities(text: str, pattern: tuple[int, ...]) -> int:
    if not pattern:
        return 0 if "#" in text else 1

    if len(text) < sum(pattern) + len(pattern) - 1:
        return 0

    # Cases where the next run does not start here.
    total = 0
    if text[0] != "#":
        total += possibilities(text[1:], pattern)

    # Cases where the next run does start here.
    run = pattern[0]
    if "." not in text[:run] and (len(text) == run or text[run] != "#"):
        total += possibilities(text[run + 1 :], pattern[1:])

    return total


def solve() -> None:
    puzzle = data_dir() / "day12.txt"
    data = puzzle.read_text(encoding="utf-8")
    records = [Record.from_string(line) for line in data.splitlines()]

    part_one = sum(possibilities(r.line, r.pattern) for r in records)
    print(f"Part one: {part_one}")

    part_two = sum(
        possibilities("?".join([r.line] * 5), r.pattern * 5) for r in records
    )
    print(f"Part two: {part_two}")
