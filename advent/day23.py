from __future__ import annotations

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

TURNS = {
    "^": [NORTH],
    "v": [SOUTH],
    ">": [EAST],
    "<": [WEST],
    ".": [NORTH, SOUTH, EAST, WEST],
}


Grid: TypeAlias = dict[Coord2, str]


@frozen
class Layout:
    grid: Grid

    @staticmethod
    def from_string(text: str) -> Layout:
        grid = {
            (row, col): char
            for row, line in enumerate(text.splitlines())
            for col, char in enumerate(line)
            if char != "#"
        }

        return Layout(grid)

    def neighbours(self, tile: Coord2, *, part_two: bool = False) -> Iterator[Coord2]:
        row, col = tile
        content = "." if part_two else self.grid[tile]
        directions = TURNS[content]

        for drow, dcol in directions:
            new_row = row + drow
            new_col = col + dcol
            if (new_row, new_col) not in self.grid:
                continue

            yield (new_row, new_col)

    def direct_paths(
        self, tiles: set[Coord2], *, part_two: bool = False
    ) -> dict[Coord2, list[tuple[Coord2, int]]]:
        paths: dict[Coord2, list[tuple[Coord2, int]]] = defaultdict(list)
        for start in tiles:
            visited: set[Coord2] = set()
            stack = [(0, start)]
            while stack:
                distance, tile = stack.pop()
                if tile in visited:
                    continue

                visited.add(tile)

                if tile != start and tile in tiles:
                    paths[start].append((tile, distance))
                    continue

                for neighbour in self.neighbours(tile, part_two=part_two):
                    stack.append((distance + 1, neighbour))

        return paths

    def solve(self, *, part_two: bool = False) -> int:
        goal = max(self.grid)
        start = min(self.grid)
        hubs = {
            tile
            for tile in self.grid
            if sum(1 for n in self.neighbours(tile, part_two=part_two)) > 2
        }
        nodes = hubs | {start, goal}
        neighbours = self.direct_paths(nodes, part_two=part_two)
        node_indexes = {tile: index for index, tile in enumerate(nodes)}

        best = 0
        stack: list[tuple[int, int, Coord2]] = [(0, 0, start)]

        while stack:
            cost, path, tile = stack.pop()
            if tile == goal:
                best = max(cost, best)
                continue

            for new_tile, cost_delta in neighbours[tile]:
                new_tile_index = node_indexes[new_tile]
                new_tile_bit = 1 << new_tile_index
                if new_tile_bit & path:
                    continue

                new_cost = cost + cost_delta
                new_path = path | new_tile_bit
                stack.append((new_cost, new_path, new_tile))

        return best


def solve() -> None:
    puzzle = data_dir() / "day23.txt"
    data = puzzle.read_text(encoding="utf-8")

    layout = Layout.from_string(data)
    part_one = layout.solve()
    print(f"Part one: {part_one}")

    part_two = layout.solve(part_two=True)
    print(f"Part two: {part_two}")
