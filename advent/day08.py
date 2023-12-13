from __future__ import annotations

import itertools
import math

from attrs import frozen

from advent.utils import data_dir


@frozen
class Node:
    name: str
    left: str
    right: str

    @staticmethod
    def from_string(string: str) -> Node:
        name, nodes = string.split(" = ")
        left, right = nodes.split(", ")
        return Node(name, left[1:], right[:-1])


def solve() -> None:
    puzzle = data_dir() / "day08.txt"
    data = puzzle.read_text(encoding="utf-8")
    lines = data.splitlines()

    instructions = lines[0]
    nodes = [Node.from_string(line) for line in data.splitlines()[2:]]
    node_map = {node.name: node for node in nodes}

    position = "AAA"
    count = 0
    for instruction in itertools.cycle(instructions):
        if position == "ZZZ":
            break

        count += 1
        node = node_map[position]
        position = node.left if instruction == "L" else node.right

    print(f"Part one: {count}")

    starts = {node.name for node in nodes if node.name.endswith("A")}
    lengths: list[int] = []
    for start in starts:
        position = start
        count = 0
        for instruction in itertools.cycle(instructions):
            if position.endswith("Z"):
                lengths.append(count)
                break

            count += 1
            node = node_map[position]
            position = node.left if instruction == "L" else node.right

    part_two = math.lcm(*lengths)
    print(f"Part two: {part_two}")
