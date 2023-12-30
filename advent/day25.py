from __future__ import annotations

import math
import random
from collections import Counter
from typing import TypeAlias

from advent.utils import UnionFind, data_dir

Node: TypeAlias = str
Edge: TypeAlias = tuple[Node, Node]


def karger(nodes: set[Node], edges: list[Edge]) -> tuple[UnionFind[Node], list[Edge]]:
    uf = UnionFind.from_elements(nodes)
    random.shuffle(edges)

    edge_iter = iter(edges)
    components = len(nodes)
    while components > 2:
        edge = next(edge_iter)
        if uf.union(*edge):
            components -= 1

    cut = [(a, b) for a, b in edge_iter if uf.find(a) != uf.find(b)]

    return uf, cut


def solve() -> None:
    puzzle = data_dir() / "day25.txt"
    data = puzzle.read_text(encoding="utf-8")

    nodes: set[Node] = set()
    edges: list[Edge] = []

    for line in data.splitlines():
        node, neighbours = line.split(": ")
        nodes.add(node)
        for neighbour in neighbours.split():
            nodes.add(neighbour)
            edges.append((node, neighbour))

    while True:
        uf, cut = karger(nodes, edges)
        if len(cut) == 3:
            break

    counter = Counter(uf.find(node) for node in nodes)

    part_one = math.prod(counter.values())
    print(f"Part one: {part_one}")
