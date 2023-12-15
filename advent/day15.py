from __future__ import annotations

from collections import defaultdict

from advent.utils import data_dir


def advent_hash(text: str) -> int:
    value = 0
    for c in text:
        value += ord(c)
        value *= 17
        value %= 256

    return value


def solve() -> None:
    puzzle = data_dir() / "day15.txt"
    data = puzzle.read_text(encoding="utf-8")

    steps = data.strip().split(",")
    hashes = (advent_hash(step) for step in steps)
    part_one = sum(hashes)
    print(f"Part one: {part_one}")

    boxes: dict[int, list[tuple[str, int]]] = defaultdict(list)
    for lens in steps:
        if lens.endswith("-"):
            label = lens[:-1]
        else:
            label, number = lens.split("=")

        index = advent_hash(label)
        box = boxes[index]

        if lens.endswith("-"):
            boxes[index] = [v for v in box if v[0] != label]
        else:
            for i, v in enumerate(box):
                if v[0] == label:
                    box[i] = (label, int(number))
                    break
            else:
                box.append((label, int(number)))

    powers = (
        (box_number + 1) * slot * focal_length
        for box_number, box in boxes.items()
        for slot, (_, focal_length) in enumerate(box, 1)
    )

    part_two = sum(powers)
    print(f"Part two: {part_two}")
