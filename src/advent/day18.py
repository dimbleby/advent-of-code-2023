from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from advent.utils import data_dir

if TYPE_CHECKING:
    from advent.utils import Coord2

DIRECTIONS = {"R": (0, 1), "D": (1, 0), "L": (0, -1), "U": (-1, 0)}


@dataclass(frozen=True)
class Instruction:
    direction: str
    distance: int
    colour: str

    @staticmethod
    def from_string(line: str) -> Instruction:
        parts = line.split()
        return Instruction(parts[0], int(parts[1]), parts[2][1:-1])

    def colour_direction(self) -> str:
        index = int(self.colour[-1])
        return "RDLU"[index]

    def colour_distance(self) -> int:
        return int(self.colour[1:-1], 16)

    def real_direction(self, *, part_two: bool = False) -> Coord2:
        rdlu = self.colour_direction() if part_two else self.direction
        return DIRECTIONS[rdlu]

    def real_distance(self, *, part_two: bool = False) -> int:
        return self.colour_distance() if part_two else self.distance


def build_loop(
    instructions: list[Instruction], *, part_two: bool = False
) -> tuple[list[Coord2], int]:
    corners: list[Coord2] = []
    length = 0

    row, col = (0, 0)
    for instruction in instructions:
        edge_length = instruction.real_distance(part_two=part_two)
        drow, dcol = instruction.real_direction(part_two=part_two)
        row += drow * edge_length
        col += dcol * edge_length
        corners.append((row, col))
        length += edge_length

    return corners, length


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
    puzzle = data_dir() / "day18.txt"
    data = puzzle.read_text(encoding="utf-8")

    instructions = [Instruction.from_string(line) for line in data.splitlines()]

    # Day 10 redux.
    corners, length = build_loop(instructions)
    part_one = get_area(corners) + (length // 2) + 1
    print(f"Part one: {part_one}")

    corners, length = build_loop(instructions, part_two=True)
    part_two = get_area(corners) + (length // 2) + 1
    print(f"Part two: {part_two}")
