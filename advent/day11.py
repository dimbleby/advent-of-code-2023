from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from advent.utils import data_dir, manhattan

if TYPE_CHECKING:
    from advent.utils import Coord2


def recalibrate(galaxies: set[Coord2], *, expansion: int = 2) -> set[Coord2]:
    occupied_rows = {r for r, _ in galaxies}
    rows = max(occupied_rows)
    row_sizes = [1 if r in occupied_rows else expansion for r in range(rows)]
    row_coords = list(itertools.accumulate(row_sizes, initial=0))

    occupied_cols = {c for _, c in galaxies}
    cols = max(occupied_cols)
    col_sizes = [1 if c in occupied_cols else expansion for c in range(cols)]
    col_coords = list(itertools.accumulate(col_sizes, initial=0))

    return {(row_coords[r], col_coords[c]) for (r, c) in galaxies}


def solve() -> None:
    puzzle = data_dir() / "day11.txt"
    data = puzzle.read_text(encoding="utf-8")

    galaxies: set[Coord2] = set()
    for row, line in enumerate(data.splitlines()):
        for col, char in enumerate(line):
            if char == "#":
                galaxies.add((row, col))

    expanded = recalibrate(galaxies)
    part_one = sum(manhattan(g1, g2) for g1, g2 in itertools.combinations(expanded, 2))
    print(f"Part one: {part_one}")

    expanded = recalibrate(galaxies, expansion=1000000)
    part_two = sum(manhattan(g1, g2) for g1, g2 in itertools.combinations(expanded, 2))
    print(f"Part two: {part_two}")
