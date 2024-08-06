from __future__ import annotations

import itertools

from advent.utils import data_dir


def extrapolate(sequence: list[int], *, backwards: bool = False) -> int:
    if all(n == 0 for n in sequence):
        return 0

    differences = [b - a for a, b in itertools.pairwise(sequence)]
    next_difference = extrapolate(differences, backwards=backwards)
    return (
        sequence[0] - next_difference if backwards else sequence[-1] + next_difference
    )


def solve() -> None:
    puzzle = data_dir() / "day09.txt"
    data = puzzle.read_text(encoding="utf-8")
    sequences = [[int(n) for n in line.split()] for line in data.splitlines()]

    extrapolations = (extrapolate(sequence) for sequence in sequences)
    part_one = sum(extrapolations)
    print(f"Part one: {part_one}")

    extrapolations = (extrapolate(sequence, backwards=True) for sequence in sequences)
    part_two = sum(extrapolations)
    print(f"Part two: {part_two}")
