from __future__ import annotations

from attrs import field, frozen

from advent.utils import Coord2, data_dir

type Grid = list[str]
type State = tuple[Coord2, Coord2]

NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)
DIRECTION_INDEX = {NORTH: 0, SOUTH: 1, EAST: 2, WEST: 3}

TURNS = {
    "-": [[EAST, WEST], [EAST, WEST], [EAST], [WEST]],
    "|": [[NORTH], [SOUTH], [NORTH, SOUTH], [NORTH, SOUTH]],
    "/": [[EAST], [WEST], [NORTH], [SOUTH]],
    "\\": [[WEST], [EAST], [SOUTH], [NORTH]],
    ".": [[NORTH], [SOUTH], [EAST], [WEST]],
}


@frozen
class Layout:
    grid: Grid
    rows: int = field(init=False)
    cols: int = field(init=False)

    def __attrs_post_init__(self) -> None:
        rows = len(self.grid)
        cols = len(self.grid[0])
        object.__setattr__(self, "rows", rows)
        object.__setattr__(self, "cols", cols)

    @staticmethod
    def from_string(text: str) -> Layout:
        grid = text.splitlines()
        return Layout(grid)

    def energize(self, start: State = ((0, 0), EAST)) -> int:
        count = 0
        visited = [0] * self.rows * self.cols
        stack = [start]
        while stack:
            state = stack.pop()
            (row, col), direction = state

            pos_index = row * self.cols + col
            dir_index = DIRECTION_INDEX[direction]
            dir_bit = 1 << dir_index
            if visited[pos_index] & dir_bit:
                continue

            if visited[pos_index] == 0:
                count += 1

            visited[pos_index] |= dir_bit

            content = self.grid[row][col]
            for drow, dcol in TURNS[content][dir_index]:
                new_row, new_col = row + drow, col + dcol

                if not 0 <= new_row < self.rows:
                    continue

                if not 0 <= new_col < self.cols:
                    continue

                stack.append(((new_row, new_col), (drow, dcol)))

        return count

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
