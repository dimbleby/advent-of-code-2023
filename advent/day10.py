from __future__ import annotations

from typing import TypeAlias

from advent.utils import Coord2, data_dir

Grid: TypeAlias = dict[Coord2, str]

NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)

TURNS = {
    "-": {EAST: EAST, WEST: WEST},
    "J": {EAST: NORTH, SOUTH: WEST},
    "7": {EAST: SOUTH, NORTH: WEST},
    "F": {NORTH: EAST, WEST: SOUTH},
    "|": {NORTH: NORTH, SOUTH: SOUTH},
    "L": {SOUTH: EAST, WEST: NORTH},
}


def find_loop_going(
    grid: Grid, start: Coord2, direction: Coord2
) -> list[Coord2] | None:
    loop = [start]
    row, col = start
    drow, dcol = direction

    while True:
        row += drow
        col += dcol
        if (row, col) == start:
            return loop
        loop.append((row, col))

        value = grid.get((row, col))
        if value is None:
            # Gone off the edge of the grid.
            return None

        turntable = TURNS.get(value)
        if turntable is None:
            # Entered a tile with no pipe.
            return None

        new_direction = turntable.get((drow, dcol))
        if new_direction is None:
            # Entered a tile whose pipe does not join our loop.
            return None

        drow, dcol = new_direction

    raise AssertionError


def find_loop(grid: Grid, start: Coord2) -> list[Coord2]:
    for starting_direction in (NORTH, SOUTH, EAST, WEST):
        loop = find_loop_going(grid, start, starting_direction)
        if loop is not None:
            return loop

    raise AssertionError


def get_area(loop: list[Coord2]) -> int:
    # https://en.wikipedia.org/wiki/Shoelace_formula
    value = 0
    for j in range(len(loop)):
        xi, yi = loop[j - 1]
        xj, yj = loop[j]
        value += (xi * yj) - (xj * yi)

    # Area is obviously an integer.
    value = abs(value)
    return value // 2


def solve() -> None:
    puzzle = data_dir() / "day10.txt"
    data = puzzle.read_text(encoding="utf-8")

    grid: Grid = {}
    start: Coord2
    for row, line in enumerate(data.splitlines()):
        for col, char in enumerate(line):
            grid[(row, col)] = char
            if char == "S":
                start = (row, col)

    # Loop is of even length - every step north must be undone by a matching step south,
    # and so on.
    loop = find_loop(grid, start)
    part_one = len(loop) // 2
    print(f"Part one: {part_one}")

    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    #
    # But this is an easy special case:
    # - straight lines on the boundary contribute 0.5 to the area
    # - right turns contribute 0.25
    # - left turns contribute 0.75
    # - there are four more right than left turns
    #
    # giving (of course!) the same answer.
    area = get_area(loop)
    part_two = area - part_one + 1
    print(f"Part two: {part_two}")
