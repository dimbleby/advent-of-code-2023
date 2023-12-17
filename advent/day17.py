from __future__ import annotations

import heapq
from collections import defaultdict
from typing import TYPE_CHECKING, TypeAlias

from attrs import frozen

from advent.utils import Coord2, data_dir

if TYPE_CHECKING:
    from collections.abc import Iterator

NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)


Grid: TypeAlias = dict[Coord2, int]

# boolean for whether we are moving north-south, or east-west.
State: TypeAlias = tuple[Coord2, bool]


@frozen
class Layout:
    grid: Grid

    @staticmethod
    def from_string(text: str) -> Layout:
        grid = {
            (row, col): int(char)
            for row, line in enumerate(text.splitlines())
            for col, char in enumerate(line)
        }

        return Layout(grid)

    # Returns new state, and cost of getting to that new state.
    def neighbours(
        self, state: State, *, part_two: bool = False
    ) -> Iterator[tuple[State, int]]:
        position, north_south = state
        for drow, dcol in (NORTH, SOUTH) if north_south else (EAST, WEST):
            new_row, new_col = position
            cost = 0

            lo, hi = (4, 10) if part_two else (1, 3)
            for step in range(1, hi + 1):
                new_row += drow
                new_col += dcol
                new_position = (new_row, new_col)

                step_cost = self.grid.get(new_position)
                if step_cost is None:
                    break

                cost += step_cost

                if step < lo:
                    continue

                yield (new_position, not north_south), cost

    def solve(self, *, part_two: bool = False) -> int:
        goal = max(self.grid)
        start = (0, 0)

        queue: list[tuple[int, State]] = [(0, (start, True)), (0, (start, False))]
        heapq.heapify(queue)
        costs: dict[State, int] = defaultdict(lambda: 100000)

        while queue:
            cost, state = heapq.heappop(queue)

            if cost > costs[state]:
                continue

            if state[0] == goal:
                return cost

            for new_state, cost_delta in self.neighbours(state, part_two=part_two):
                new_cost = cost + cost_delta
                if new_cost < costs[new_state]:
                    costs[new_state] = new_cost
                    heapq.heappush(queue, (new_cost, new_state))

        raise AssertionError


def solve() -> None:
    puzzle = data_dir() / "day17.txt"
    data = puzzle.read_text(encoding="utf-8")

    layout = Layout.from_string(data)
    part_one = layout.solve()
    print(f"Part one: {part_one}")

    part_two = layout.solve(part_two=True)
    print(f"Part two: {part_two}")
