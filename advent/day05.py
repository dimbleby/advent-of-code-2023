from __future__ import annotations

import itertools

from attrs import frozen

from advent.utils import chunks, data_dir


@frozen
class Range:
    start: int
    length: int


@frozen
class Map:
    dest: int
    source: int
    length: int

    @staticmethod
    def from_string(string: str) -> Map:
        numbers = (int(n) for n in string.split())
        return Map(*numbers)

    def plumb(self, start: int) -> int | None:
        if self.source <= start < self.source + self.length:
            return start + self.dest - self.source

        return None

    def plumb_range(self, range_: Range) -> tuple[list[Range], list[Range]]:
        # Describe ranges as (lo, hi): exclusive at upper end.
        map_lo, map_hi = self.source, self.source + self.length
        range_lo, range_hi = range_.start, range_.start + range_.length

        # Calculate boundaries: what part of the range is below this map, overlaps it,
        # above this map?
        lo_hi = min(range_hi, map_lo)
        overlap_lo = max(range_lo, map_lo)
        overlap_hi = min(range_hi, map_hi)
        hi_lo = max(range_lo, map_hi)

        # Accordingly, what part of the range is moved and unmoved?
        moved: list[Range] = []
        unmoved: list[Range] = []
        if range_lo < lo_hi:
            unmoved.append(Range(range_lo, lo_hi - range_lo))

        if overlap_lo < overlap_hi:
            moved.append(
                Range(overlap_lo + self.dest - self.source, overlap_hi - overlap_lo)
            )

        if hi_lo < range_hi:
            unmoved.append(Range(hi_lo, range_hi - hi_lo))

        return moved, unmoved

    def plumb_ranges(self, ranges: list[Range]) -> tuple[list[Range], list[Range]]:
        moved: list[Range] = []
        unmoved: list[Range] = []
        for r in ranges:
            m, u = self.plumb_range(r)
            moved += m
            unmoved += u

        return moved, unmoved


@frozen
class Block:
    maps: list[Map]

    @staticmethod
    def from_lines(lines: list[str]) -> Block:
        maps = [Map.from_string(line) for line in lines[1:]]
        return Block(maps)

    def plumb(self, start: int) -> int:
        for m in self.maps:
            out = m.plumb(start)
            if out is not None:
                return out

        return start

    def plumb_ranges(self, ranges: list[Range]) -> list[Range]:
        moved: list[Range] = []
        unmoved = ranges
        for m in self.maps:
            new_moved, unmoved = m.plumb_ranges(unmoved)
            moved += new_moved

        return moved + unmoved


@frozen
class Chain:
    blocks: list[Block]

    def plumb(self, start: int) -> int:
        value = start
        for block in self.blocks:
            value = block.plumb(value)

        return value

    def plumb_ranges(self, ranges: list[Range]) -> list[Range]:
        output = ranges
        for block in self.blocks:
            output = block.plumb_ranges(output)

        return output


def solve() -> None:
    puzzle = data_dir() / "day05.txt"
    data = puzzle.read_text(encoding="utf-8").strip()
    lines = data.splitlines()

    seeds_, values = lines[0].split(": ")
    seeds = [int(n) for n in values.split()]

    sections = [
        list(section) for key, section in itertools.groupby(lines[1:], key=bool) if key
    ]
    blocks = [Block.from_lines(section) for section in sections]
    chain = Chain(blocks)

    locations = [chain.plumb(seed) for seed in seeds]
    part_one = min(locations)
    print(f"Part one: {part_one}")

    seed_ranges = [Range(*numbers) for numbers in chunks(seeds, 2)]
    output_ranges = chain.plumb_ranges(seed_ranges)
    part_two = min(r.start for r in output_ranges)
    print(f"Part two: {part_two}")
