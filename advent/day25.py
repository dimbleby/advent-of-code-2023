from __future__ import annotations

import random
from collections import Counter, defaultdict
from typing import TypeAlias

from advent.utils import UnionFind, data_dir

Edge: TypeAlias = tuple[str, str]


def karger(graph: dict[str, list[str]]) -> tuple[UnionFind[str], list[Edge]]:
    uf = UnionFind.from_elements(graph)

    edge_list: list[Edge] = [
        (a, b) for a, neighbours in graph.items() for b in neighbours if a < b
    ]
    random.shuffle(edge_list)
    edges = iter(edge_list)

    components = len(graph)
    while components > 2:
        edge = next(edges)
        if uf.union(*edge):
            components -= 1

    cut = [(a, b) for a, b in edges if uf.find(a) != uf.find(b)]

    return uf, cut


def solve() -> None:
    puzzle = data_dir() / "day25.txt"
    data = puzzle.read_text(encoding="utf-8")

    graph: dict[str, list[str]] = defaultdict(list)
    for line in data.splitlines():
        node, neighbours = line.split(": ")
        for neighbour in neighbours.split():
            graph[node].append(neighbour)
            graph[neighbour].append(node)

    uf: UnionFind[str]
    while True:
        uf, cut = karger(graph)
        if len(cut) == 3:
            break

    counter = Counter(uf.find(node) for node in graph)

    part_one = 1
    for value in counter.values():
        part_one *= value

    print(f"Part one: {part_one}")
