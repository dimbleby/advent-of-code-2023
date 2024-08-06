from __future__ import annotations

import itertools
import math
from dataclasses import dataclass

from advent.utils import Vec3, data_dir


@dataclass
class Stone:
    pos: Vec3
    vel: Vec3

    @staticmethod
    def from_string(text: str) -> Stone:
        position, velocity = text.split(" @ ")
        x, y, z = (int(w) for w in position.split(", "))
        dx, dy, dz = (int(w) for w in velocity.split(", "))
        return Stone(Vec3(x, y, z), Vec3(dx, dy, dz))

    def __sub__(self, other: Stone) -> Stone:
        return Stone(self.pos - other.pos, self.vel - other.vel)


def cross_part_one(s1: Stone, s2: Stone) -> bool:
    # First line is s1 + t1 * v1
    # Second line is s2 + t2 * v2
    #
    # Find when and where they meet.
    #
    # s2 - s1 = t1 * v1 - t2 * v2
    det = s1.vel.cross(s2.vel).z
    if det == 0:
        return False

    s = s2 - s1
    t1 = s.pos.cross(s2.vel).z / det
    if t1 < 0:
        return False

    t2 = s.pos.cross(s1.vel).z / det
    if t2 < 0:
        return False

    x = s1.pos.x + t1 * s1.vel.x
    if not 200000000000000 <= x <= 400000000000000:
        return False

    y = s1.pos.y + t1 * s1.vel.y
    if not 200000000000000 <= y <= 400000000000000:  # noqa: SIM103
        return False

    return True


def collide_part_two(stones: list[Stone]) -> int:
    # Work in the frame of reference of the first stone.
    s0 = stones[0]
    s1 = stones[1] - s0
    s2 = stones[2] - s0

    # The rock passes through the origin (stone 0) and hits the line given by stone 1.
    #
    # Therefore it travels in the plane with normal s1.pos x s1.vel.
    normal = s1.pos.cross(s1.vel)
    normal //= math.gcd(normal.x, normal.y, normal.z)

    # The rock must hit stone 2 when it crosses that plane.
    # ie when (s2.pos + t2 * s2.vel) . normal == 0
    t2 = -s2.pos.dot(normal) // s2.vel.dot(normal)
    x2 = s2.pos + t2 * s2.vel

    # The rock's path takes it through the origin and x2: where does it meet s1?
    #
    # l * x2 = s1.pos + t1 * s1.vel
    t1 = s1.pos.cross(x2).z // x2.cross(s1.vel).z
    x1 = s1.pos + t1 * s1.vel

    # Now it's easy to get the rock's velocity, and position at time 0.
    rvel = (x2 - x1) // (t2 - t1)
    rpos = x1 - t1 * rvel

    # Undo the change of frame.
    rpos += s0.pos
    return rpos.x + rpos.y + rpos.z


def solve() -> None:
    puzzle = data_dir() / "day24.txt"
    data = puzzle.read_text(encoding="utf-8")

    stones = [Stone.from_string(line) for line in data.splitlines()]

    part_one = sum(itertools.starmap(cross_part_one, itertools.combinations(stones, 2)))
    print(f"Part one: {part_one}")

    part_two = collide_part_two(stones)
    print(f"Part two: {part_two}")
