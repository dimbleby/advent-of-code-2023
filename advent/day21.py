from __future__ import annotations

import itertools
from collections import deque
from typing import TYPE_CHECKING

from attrs import field, frozen

from advent.utils import Coord2, data_dir

if TYPE_CHECKING:
    from collections.abc import Iterator

NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)


type Grid = dict[Coord2, str]


@frozen
class Layout:
    grid: Grid
    start: Coord2 = field(init=False)
    num_rows: int = field(init=False)
    num_cols: int = field(init=False)

    def __attrs_post_init__(self) -> None:
        start = next(k for k, v in self.grid.items() if v == "S")
        max_row, max_col = max(self.grid)
        object.__setattr__(self, "start", start)
        object.__setattr__(self, "num_rows", max_row + 1)
        object.__setattr__(self, "num_cols", max_col + 1)

    @staticmethod
    def from_string(text: str) -> Layout:
        grid = {
            (row, col): char
            for row, line in enumerate(text.splitlines())
            for col, char in enumerate(line)
        }

        return Layout(grid)

    def neighbours(self, state: Coord2) -> Iterator[Coord2]:
        row, col = state
        for drow, dcol in (NORTH, SOUTH, EAST, WEST):
            new_row = row + drow
            new_col = col + dcol
            new_position = new_row, new_col

            effective_row = new_row % self.num_rows
            effective_col = new_col % self.num_cols

            if self.grid[(effective_row, effective_col)] != "#":
                yield new_position

    def solve(self, steps: int, target: int) -> tuple[int, list[int]]:
        part_one: int | None = None
        sequence: list[int] = []

        visited: set[Coord2] = set()
        queue: deque[tuple[int, Coord2]] = deque([(0, self.start)])

        next_checkpoint = target % self.num_cols
        while queue:
            cost, position = queue.popleft()
            if part_one is None and cost > steps:
                part_one = sum((row + col + cost) % 2 for row, col in visited)

            if cost > next_checkpoint:
                value = sum((row + col + cost) % 2 for row, col in visited)
                sequence.append(value)
                next_checkpoint += self.num_cols

            if part_one is not None and len(sequence) > 2:
                return part_one, sequence

            if position in visited:
                continue

            visited.add(position)

            queue.extend((cost + 1, new_pos) for new_pos in self.neighbours(position))

        raise AssertionError


def solve() -> None:
    puzzle = data_dir() / "day21.txt"
    data = puzzle.read_text(encoding="utf-8")

    layout = Layout.from_string(data)
    part_one, sequence = layout.solve(64, 26501365)
    print(f"Part one: {part_one}")

    diff1 = [j - i for i, j in itertools.pairwise(sequence)]
    diff2 = [j - i for i, j in itertools.pairwise(diff1)]
    a = diff2[0] // 2  # it's an integer, I checked...
    b = diff1[0] - a
    c = sequence[0]
    n = 26501365 // layout.num_cols
    part_two = a * n * n + b * n + c
    print(f"Part two: {part_two}")
