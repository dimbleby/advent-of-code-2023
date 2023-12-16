from __future__ import annotations

from typing import TYPE_CHECKING, TypeAlias

from attrs import field, frozen

from advent.utils import Coord2, data_dir

if TYPE_CHECKING:
    from collections.abc import Iterator

Grid: TypeAlias = dict[Coord2, str]
State: TypeAlias = tuple[Coord2, Coord2]

NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)

TURNS = {
    "-": {NORTH: [EAST, WEST], SOUTH: [EAST, WEST], EAST: [EAST], WEST: [WEST]},
    "|": {NORTH: [NORTH], SOUTH: [SOUTH], EAST: [NORTH, SOUTH], WEST: [NORTH, SOUTH]},
    "/": {NORTH: [EAST], SOUTH: [WEST], EAST: [NORTH], WEST: [SOUTH]},
    "\\": {NORTH: [WEST], SOUTH: [EAST], EAST: [SOUTH], WEST: [NORTH]},
    ".": {NORTH: [NORTH], SOUTH: [SOUTH], EAST: [EAST], WEST: [WEST]},
}


@frozen
class Layout:
    grid: Grid
    rows: int = field(init=False)
    cols: int = field(init=False)

    def __attrs_post_init__(self) -> None:
        object.__setattr__(self, "rows", 1 + max(r for r, _ in self.grid))
        object.__setattr__(self, "cols", 1 + max(c for _, c in self.grid))

    @staticmethod
    def from_string(text: str) -> Layout:
        grid: Grid = {}
        for row, line in enumerate(text.splitlines()):
            for col, char in enumerate(line):
                grid[(row, col)] = char

        return Layout(grid)

    def neighbours(self, state: State) -> Iterator[State]:
        place, direction = state
        content = self.grid[place]
        (row, col) = place
        for new_direction in TURNS[content][direction]:
            drow, dcol = new_direction
            new_row, new_col = row + drow, col + dcol

            if not 0 <= new_row < self.rows:
                continue

            if not 0 <= new_col < self.cols:
                continue

            yield ((new_row, new_col), new_direction)

    def energize(self, start: State = ((0, 0), EAST)) -> int:
        visited: set[State] = set()
        stack = [start]
        while stack:
            state = stack.pop()
            if state in visited:
                continue

            visited.add(state)

            neighbours = self.neighbours(state)
            stack.extend(neighbours)

        places = {place for place, _ in visited}
        return len(places)

    def most_energized(self) -> int:
        lefts = (((row, 0), EAST) for row in range(self.rows))
        rights = (((row, self.cols - 1), WEST) for row in range(self.rows))
        downs = (((0, col), SOUTH) for col in range(self.cols))
        ups = (((self.rows - 1, col), NORTH) for col in range(self.cols))

        lights = (self.energize(start) for start in (*lefts, *rights, *downs, *ups))
        return max(lights)


def solve() -> None:
    puzzle = data_dir() / "day16.txt"
    data = puzzle.read_text(encoding="utf-8")

    layout = Layout.from_string(data)

    part_one = layout.energize()
    print(f"Part one: {part_one}")

    part_two = layout.most_energized()
    print(f"Part two: {part_two}")
