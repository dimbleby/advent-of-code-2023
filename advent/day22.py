from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from attrs import define, field

from advent.utils import data_dir

if TYPE_CHECKING:
    from advent.utils import Coord3


@define
class Range:
    lo: int
    hi: int  # Exclusive.


@define
class Brick:
    index: int
    x: Range
    y: Range
    z: Range

    @staticmethod
    def from_string(index: int, text: str) -> Brick:
        los, his = text.split("~")
        xlo, ylo, zlo = (int(n) for n in los.split(","))
        xhi, yhi, zhi = (int(n) for n in his.split(","))

        return Brick(
            index=index,
            x=Range(xlo, xhi + 1),
            y=Range(ylo, yhi + 1),
            z=Range(zlo, zhi + 1),
        )


@define
class Tower:
    bricks: list[Brick]
    occupied: dict[Coord3, int] = field(init=False)

    def __attrs_post_init__(self) -> None:
        self.occupied = {
            cell: brick.index
            for brick in self.bricks
            for cell in itertools.product(
                range(brick.x.lo, brick.x.hi),
                range(brick.y.lo, brick.y.hi),
                range(brick.z.lo, brick.z.hi),
            )
        }

    def drop(self, brick: Brick) -> None:
        for fall in range(brick.z.lo):
            support = (
                (x, y, brick.z.lo - fall - 1)
                for x, y in itertools.product(
                    range(brick.x.lo, brick.x.hi), range(brick.y.lo, brick.y.hi)
                )
            )
            if any(cell in self.occupied for cell in support):
                break

        if fall == 0:
            return

        for x, y, z in itertools.product(
            range(brick.x.lo, brick.x.hi),
            range(brick.y.lo, brick.y.hi),
            range(brick.z.lo, brick.z.hi),
        ):
            self.occupied.pop((x, y, z))

        brick.z.lo -= fall
        brick.z.hi -= fall

        for x, y, z in itertools.product(
            range(brick.x.lo, brick.x.hi),
            range(brick.y.lo, brick.y.hi),
            range(brick.z.lo, brick.z.hi),
        ):
            self.occupied[(x, y, z)] = brick.index

    def settle(self) -> None:
        for brick in sorted(self.bricks, key=lambda brick: brick.z.lo):
            self.drop(brick)

    def supporting_below(self, brick: Brick) -> set[int]:
        lower = (
            (x, y, brick.z.lo - 1)
            for x, y in itertools.product(
                range(brick.x.lo, brick.x.hi), range(brick.y.lo, brick.y.hi)
            )
        )

        below = set()
        for cell in lower:
            index = self.occupied.get(cell)
            if index is not None:
                below.add(index)

        return below

    def supported_above(self, brick: Brick) -> set[int]:
        upper = (
            (x, y, brick.z.hi)
            for x, y in itertools.product(
                range(brick.x.lo, brick.x.hi), range(brick.y.lo, brick.y.hi)
            )
        )

        above = set()
        for cell in upper:
            index = self.occupied.get(cell)
            if index is not None:
                above.add(index)

        return above


def solve() -> None:
    puzzle = data_dir() / "day22.txt"
    data = puzzle.read_text(encoding="utf-8")

    bricks = list(itertools.starmap(Brick.from_string, enumerate(data.splitlines())))

    tower = Tower(bricks)
    tower.settle()

    below = {brick.index: tower.supporting_below(brick) for brick in tower.bricks}
    above = {brick.index: tower.supported_above(brick) for brick in tower.bricks}

    required = {b for bs in below.values() for b in bs if len(bs) == 1}
    part_one = len(bricks) - len(required)
    print(f"Part one: {part_one}")

    part_two = 0
    for start in required:
        disintegrated: set[int] = set()
        stack = [start]
        while stack:
            brick = stack.pop()
            disintegrated.add(brick)
            for brick_above in above[brick]:
                supports = below[brick_above]
                if supports <= disintegrated:
                    stack.append(brick_above)

        part_two += len(disintegrated) - 1

    print(f"Part two: {part_two}")
