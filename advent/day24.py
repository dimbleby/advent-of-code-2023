from __future__ import annotations

import itertools

from attrs import define
from sympy import solve as ssolve
from sympy import symbols

from advent.utils import data_dir


@define
class Stone:
    x: int
    y: int
    z: int
    dx: int
    dy: int
    dz: int

    @staticmethod
    def from_string(text: str) -> Stone:
        position, velocity = text.split(" @ ")
        x, y, z = (int(w) for w in position.split(", "))
        dx, dy, dz = (int(w) for w in velocity.split(", "))
        return Stone(x, y, z, dx, dy, dz)


def cross_part_one(s1: Stone, s2: Stone) -> bool:
    # First line is s1 + t1 * v1
    # Second line is s2 + t2 * v2
    #
    # Find when and where they cross.
    #
    # s1 - s2 = t1 * v1 + t2 * v2
    det = s1.dx * s2.dy - s1.dy * s2.dx
    if det == 0:
        return False

    s = (s1.x - s2.x, s1.y - s2.y)
    t1 = (s[1] * s2.dx - s[0] * s2.dy) / det
    if t1 < 0:
        return False

    t2 = (s[1] * s1.dx - s[0] * s1.dy) / det
    if t2 < 0:
        return False

    x = s1.x + t1 * s1.dx
    if not 200000000000000 <= x <= 400000000000000:
        return False

    y = s1.y + t1 * s1.dy
    if not 200000000000000 <= y <= 400000000000000:
        return False

    return True


def collide_part_two(stones: list[Stone]) -> int:
    # rock is at r + t * vr
    #
    # So take three stones and solve
    #
    # r + vr * t1 = s1 + vs1 * t1
    # r + vr * t2 = s2 + vs2 * t2
    # r + vr * t3 = s3 + vs3 * t3
    #
    s1, s2, s3 = stones[:3]
    rx, ry, rz, vrx, vry, vrz, t1, t2, t3 = symbols("rx ry rz vrx vry vrz t1 t2 t3")
    exprs = [
        rx + vrx * t1 - s1.x - s1.dx * t1,
        ry + vry * t1 - s1.y - s1.dy * t1,
        rz + vrz * t1 - s1.z - s1.dz * t1,
        rx + vrx * t2 - s2.x - s2.dx * t2,
        ry + vry * t2 - s2.y - s2.dy * t2,
        rz + vrz * t2 - s2.z - s2.dz * t2,
        rx + vrx * t3 - s3.x - s3.dx * t3,
        ry + vry * t3 - s3.y - s3.dy * t3,
        rz + vrz * t3 - s3.z - s3.dz * t3,
    ]
    values = ssolve(exprs)  # type: ignore[no-untyped-call]
    return sum(values[0][variable] for variable in (rx, ry, rz))


def solve() -> None:
    puzzle = data_dir() / "day24.txt"
    data = puzzle.read_text(encoding="utf-8")

    stones = [Stone.from_string(line) for line in data.splitlines()]

    part_one = sum(itertools.starmap(cross_part_one, itertools.combinations(stones, 2)))
    print(f"Part one: {part_one}")

    part_two = collide_part_two(stones)
    print(f"Part two: {part_two}")
