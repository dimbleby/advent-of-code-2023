from __future__ import annotations

from collections.abc import Hashable
from pathlib import Path
from typing import TYPE_CHECKING, Generic, Protocol, TypeAlias, TypeVar

from attrs import define

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator
    from typing import Self


def data_dir() -> Path:
    return Path(__file__).parent.parent / "data"


class SupportsChunking(Protocol):
    def __getitem__(self, index: slice, /) -> Self: ...

    def __len__(self) -> int: ...


Chunkable = TypeVar("Chunkable", bound=SupportsChunking)


def chunks(seq: Chunkable, n: int) -> Iterator[Chunkable]:
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


Coord2: TypeAlias = tuple[int, int]
Coord3: TypeAlias = tuple[int, int, int]


def manhattan(here: Coord2, there: Coord2) -> int:
    r1, c1 = here
    r2, c2 = there
    return abs(r1 - r2) + abs(c1 - c2)


@define(eq=True)
class Vec2:
    x: int
    y: int

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: Vec2) -> Vec2:
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self.x - other.x, self.y - other.y)

    def __isub__(self, other: Vec2) -> Vec2:
        self.x -= other.x
        self.y -= other.y
        return self


@define(eq=True)
class Vec3:
    x: int
    y: int
    z: int

    def __add__(self, other: Vec3) -> Vec3:
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other: Vec3) -> Vec3:
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __sub__(self, other: Vec3) -> Vec3:
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __isub__(self, other: Vec3) -> Vec3:
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __mul__(self, n: int) -> Vec3:
        return Vec3(self.x * n, self.y * n, self.z * n)

    def __rmul__(self, n: int) -> Vec3:
        return Vec3(n * self.x, n * self.y, n * self.z)

    def __imul__(self, n: int) -> Vec3:
        self.x *= n
        self.y *= n
        self.z *= n
        return self

    def __floordiv__(self, n: int) -> Vec3:
        return Vec3(self.x // n, self.y // n, self.z // n)

    def __ifloordiv__(self, n: int) -> Vec3:
        self.x //= n
        self.y //= n
        self.z //= n
        return self

    def cross(self, other: Vec3) -> Vec3:
        return Vec3(
            self.y * other.z - other.y * self.z,
            self.z * other.x - other.z * self.x,
            self.x * other.y - other.x * self.y,
        )

    def dot(self, other: Vec3) -> int:
        return self.x * other.x + self.y * other.y + self.z * other.z


T = TypeVar("T", bound=Hashable)


@define
class UnionFind(Generic[T]):
    parents: dict[T, T]
    ranks: dict[T, int]

    @staticmethod
    def from_elements(things: Iterable[T]) -> UnionFind[T]:
        parents = {thing: thing for thing in things}
        ranks = dict.fromkeys(things, 0)
        return UnionFind(parents, ranks)

    def find(self, k: T) -> T:
        root = k
        while root != (parent := self.parents[root]):
            root = parent

        while root != (parent := self.parents[k]):
            self.parents[k] = root
            k = parent

        return root

    def union(self, a: T, b: T) -> bool:
        x = self.find(a)
        y = self.find(b)

        if x == y:
            return False

        xrank, yrank = self.ranks[x], self.ranks[y]
        if xrank < yrank:
            self.parents[x] = y
        else:
            self.parents[y] = x

            if xrank == yrank:
                self.ranks[x] = xrank + 1

        return True
