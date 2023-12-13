from __future__ import annotations

import itertools

from attrs import frozen

from advent.utils import data_dir


def mirrors(lines: list[str], mirror: int) -> bool:
    length = min(mirror, len(lines) - mirror)
    return all(lines[mirror - i - 1] == lines[mirror + i] for i in range(length))


def find_mirror(lines: list[str]) -> int | None:
    for m in range(1, len(lines)):
        if mirrors(lines, m):
            return m

    return None


def mismatches(l1: str, l2: str) -> int:
    return sum(c1 != c2 for c1, c2 in zip(l1, l2, strict=True))


def nearly_mirrors(lines: list[str], mirror: int) -> bool:
    length = min(mirror, len(lines) - mirror)
    errors = 0
    for i in range(length):
        errors += mismatches(lines[mirror - i - 1], lines[mirror + i])
        if errors > 1:
            return False

    return errors == 1


def find_near_mirror(lines: list[str]) -> int | None:
    for m in range(1, len(lines)):
        if nearly_mirrors(lines, m):
            return m

    return None


def transpose(rows: list[str]) -> list[str]:
    return ["".join(column) for column in zip(*rows, strict=True)]


@frozen
class Grid:
    rows: list[str]

    @property
    def cols(self) -> list[str]:
        return transpose(self.rows)

    def summary(self) -> int:
        row_mirror = find_mirror(self.rows)
        if row_mirror is not None:
            return 100 * row_mirror

        col_mirror = find_mirror(self.cols)
        assert col_mirror is not None
        return col_mirror

    def summary2(self) -> int:
        row_mirror = find_near_mirror(self.rows)
        if row_mirror is not None:
            return 100 * row_mirror

        col_mirror = find_near_mirror(self.cols)
        assert col_mirror is not None
        return col_mirror


def solve() -> None:
    puzzle = data_dir() / "day13.txt"
    data = puzzle.read_text(encoding="utf-8").strip()

    grids = [
        Grid(list(section))
        for key, section in itertools.groupby(data.splitlines(), key=bool)
        if key
    ]

    part_one = sum(grid.summary() for grid in grids)
    print(f"Part one: {part_one}")

    part_two = sum(grid.summary2() for grid in grids)
    print(f"Part two: {part_two}")
