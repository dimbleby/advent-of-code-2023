from __future__ import annotations

import contextlib

from advent.utils import data_dir


def get_numbers(line: str) -> list[int]:
    numbers = []
    for char in line:
        with contextlib.suppress(ValueError):
            number = int(char)
            numbers.append(number)

    return numbers


def get_numbers2(line: str) -> list[int]:
    subs = {str(n): n for n in range(1, 10)} | {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    numbers = []
    while line:
        for k, v in subs.items():
            if line.startswith(k):
                numbers.append(v)
                break

        line = line[1:]

    return numbers


def solve() -> None:
    puzzle = data_dir() / "day01.txt"
    data = puzzle.read_text(encoding="utf-8")
    lines = data.splitlines()

    numbers = [get_numbers(line) for line in lines]
    values = [10 * ns[0] + ns[-1] for ns in numbers]
    print(f"Part one: {sum(values)}")

    numbers = [get_numbers2(line) for line in lines]
    values = [10 * ns[0] + ns[-1] for ns in numbers]
    print(f"Part two: {sum(values)}")
