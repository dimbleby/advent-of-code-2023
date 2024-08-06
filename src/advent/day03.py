from __future__ import annotations

import itertools
from collections import defaultdict
from typing import TYPE_CHECKING

from advent.utils import data_dir

if TYPE_CHECKING:
    from advent.utils import Coord2


def solve() -> None:
    puzzle = data_dir() / "day03.txt"
    data = puzzle.read_text(encoding="utf-8")

    # Parse.
    grid: dict[Coord2, str] = {}
    for row, line in enumerate(data.splitlines()):
        for col, char in enumerate(line):
            grid[row, col] = char
    rows = row + 1
    cols = col + 1

    # Map out active locations, and locations next to stars.
    active: set[Coord2] = set()
    starry: dict[Coord2, Coord2] = {}  # location -> adjacent star
    for row, col in itertools.product(range(rows), range(cols)):
        if grid[row, col] in ".0123456879":
            continue

        for r, c in itertools.product((row - 1, row, row + 1), (col - 1, col, col + 1)):
            active.add((r, c))
            if grid[row, col] == "*":
                starry[r, c] = (row, col)

    # Find parts, and gears.
    parts: list[int] = []
    gears: dict[Coord2, list[int]] = defaultdict(list)  # star -> [adjacent part]

    live = False
    star: Coord2 | None = None
    number: int | None = None

    for row, col in itertools.product(range(rows), range(cols)):
        digit = grid[row, col] in "0123456789"
        if digit:
            live = live or (row, col) in active
            star = star or starry.get((row, col))
            number = number or 0
            number *= 10
            number += int(grid[row, col])

        if number is not None and (not digit or col + 1 == cols):
            if live:
                parts.append(number)
                live = False
            if star is not None:
                gears[star].append(number)
                star = None
            number = None

    part_one = sum(parts)
    print(f"Part one: {part_one}")

    part_two = sum((gs[0] * gs[1]) for gs in gears.values() if len(gs) == 2)
    print(f"Part two: {part_two}")
