#!/usr/bin/env python3

from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING

from attrs import frozen
from ortools.sat.python import cp_model

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


type Grid = dict[Coord2, str]
type Edge = tuple[Coord2, Coord2]


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

    def direct_edges(
        self, tiles: set[Coord2], *, part_two: bool = False
    ) -> dict[Edge, int]:
        edges: dict[Edge, int] = {}
        for start in tiles:
            visited: set[Coord2] = set()
            queue = deque([(0, start)])
            while queue:
                distance, tile = queue.popleft()
                if tile in visited:
                    continue

                visited.add(tile)

                if tile != start and tile in tiles:
                    edges[(start, tile)] = distance
                    continue

                queue.extend(
                    (distance + 1, neighbour)
                    for neighbour in self.neighbours(tile, part_two=part_two)
                )

        return edges

    def solve(self, *, part_two: bool = False) -> int:
        goal = max(self.grid)
        start = min(self.grid)
        hubs = {
            tile
            for tile in self.grid
            if sum(1 for n in self.neighbours(tile, part_two=part_two)) > 2
        }
        nodes = hubs | {start, goal}
        weights = self.direct_edges(nodes, part_two=part_two)

        # arcs[i, j] is true iff we travel from i to j.
        model = cp_model.CpModel()
        arcs = {edge: model.NewBoolVar("arc") for edge in weights}

        # skipped[i] is true iff we skip i.
        skipped = {node: model.NewBoolVar("skipped") for node in hubs}

        # To create a circuit constraint we add a dummy edge from goal back to start.
        indexes = {node: index for index, node in enumerate(nodes)}
        edges: list[tuple[int, int, cp_model.IntVar | bool]] = [
            (indexes[a], indexes[b], arc) for (a, b), arc in arcs.items()
        ]
        edges.extend((indexes[n], indexes[n], v) for n, v in skipped.items())
        edges.append((indexes[goal], indexes[start], True))
        model.AddCircuit(edges)

        # Objective is to maximize the weight of the selected edges.
        objective = sum(weights[edge] * arc for edge, arc in arcs.items())
        model.Maximize(objective)

        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        assert status == cp_model.OPTIMAL  # type: ignore[comparison-overlap]
        value = solver.ObjectiveValue()

        return int(value)


def solve() -> None:
    puzzle = data_dir() / "day23.txt"
    data = puzzle.read_text(encoding="utf-8")

    layout = Layout.from_string(data)
    part_one = layout.solve()
    print(f"Part one: {part_one}")

    part_two = layout.solve(part_two=True)
    print(f"Part two: {part_two}")


if __name__ == "__main__":
    solve()
