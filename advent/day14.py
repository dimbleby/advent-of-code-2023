from __future__ import annotations

from attrs import frozen

from advent.utils import data_dir


def tip_section(section: str) -> str:
    marbles = section.count("O")
    return "O" * marbles + "." * (len(section) - marbles)


def tip_section_down(section: str) -> str:
    marbles = section.count("O")
    return "." * (len(section) - marbles) + "O" * marbles


def tip_line(line: str) -> str:
    pieces = line.split("#")
    return "#".join(tip_section(piece) for piece in pieces)


def tip_line_down(line: str) -> str:
    pieces = line.split("#")
    return "#".join(tip_section_down(piece) for piece in pieces)


def transpose(rows: list[str]) -> list[str]:
    return ["".join(column) for column in zip(*rows, strict=True)]


@frozen
class Grid:
    rows: list[str]

    def tip_north(self) -> Grid:
        tipped_cols = [tip_line(col) for col in transpose(self.rows)]
        rows = transpose(tipped_cols)
        return Grid(rows)

    def tip_south(self) -> Grid:
        tipped_cols = [tip_line_down(col) for col in transpose(self.rows)]
        rows = transpose(tipped_cols)
        return Grid(rows)

    def tip_west(self) -> Grid:
        tipped_rows = [tip_line(row) for row in self.rows]
        return Grid(tipped_rows)

    def tip_east(self) -> Grid:
        tipped_rows = [tip_line_down(row) for row in self.rows]
        return Grid(tipped_rows)

    def load(self) -> int:
        loads = (
            index * row.count("O") for index, row in enumerate(reversed(self.rows), 1)
        )
        return sum(loads)

    def key(self) -> str:
        return "".join(self.rows)


def solve() -> None:
    puzzle = data_dir() / "day14.txt"
    data = puzzle.read_text(encoding="utf-8")

    lines = data.splitlines()
    grid = Grid(lines)

    tipped = grid.tip_north()
    part_one = tipped.load()
    print(f"Part one: {part_one}")

    keys: dict[str, int] = {}
    loads: list[int] = []
    cycle = 0
    while True:
        grid = grid.tip_north()
        grid = grid.tip_west()
        grid = grid.tip_south()
        grid = grid.tip_east()
        loads.append(grid.load())

        previously = keys.setdefault(grid.key(), cycle)
        if previously != cycle:
            cycle_length = cycle - previously
            break

        cycle += 1

    offset = (1000000000 - previously - 1) % cycle_length
    index = previously + offset
    part_two = loads[index]
    print(f"Part two: {part_two}")
