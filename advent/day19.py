from __future__ import annotations

import itertools
from abc import ABC, abstractmethod

from attrs import frozen
from typing_extensions import override

from advent.utils import data_dir


@frozen
class Part:
    values: dict[str, int]

    @staticmethod
    def from_text(text: str) -> Part:
        values: dict[str, int] = {}
        pieces = text[1:-1].split(",")
        for piece in pieces:
            name, value = piece.split("=")
            values[name] = int(value)

        return Part(values)

    def rating(self) -> int:
        return sum(self.values.values())


@frozen
class Range:
    lo: int
    hi: int

    def size(self) -> int:
        return self.hi - self.lo

    def split(self, split: int) -> tuple[Range | None, Range | None]:
        lo_range = hi_range = None

        lo = min(self.hi, split)
        if self.lo < lo:
            lo_range = Range(self.lo, lo)

        hi = max(split, self.lo)
        if hi < self.hi:
            hi_range = Range(hi, self.hi)

        return lo_range, hi_range


@frozen
class Parts:
    ranges: dict[str, Range]

    def volume(self) -> int:
        value = 1
        for r in self.ranges.values():
            value *= r.size()
        return value

    def split(self, variable: str, split: int) -> tuple[Parts | None, Parts | None]:
        lo_part = hi_part = None
        value_range = self.ranges[variable]
        lo_range, hi_range = value_range.split(split)

        if lo_range is not None:
            ranges = self.ranges | {variable: lo_range}
            lo_part = Parts(ranges)

        if hi_range is not None:
            ranges = self.ranges | {variable: hi_range}
            hi_part = Parts(ranges)

        return (lo_part, hi_part)


class Condition(ABC):
    @staticmethod
    def from_text(text: str) -> Condition:
        if not text:
            return AlwaysTrue()

        variable = text[0]
        condition = text[1]
        number = int(text[2:])

        if condition == "<":
            return LessThan(variable, number)

        if condition == ">":
            return GreaterThan(variable, number)

        raise AssertionError

    @abstractmethod
    def evaluate(self, part: Part) -> bool:
        ...

    @abstractmethod
    def split(self, part_range: Parts) -> tuple[Parts | None, Parts | None]:
        ...


@frozen
class AlwaysTrue(Condition):
    @override
    def evaluate(self, part: Part) -> bool:
        return True

    @override
    def split(self, part_range: Parts) -> tuple[Parts | None, Parts | None]:
        return (part_range, None)


@frozen
class LessThan(Condition):
    variable: str
    number: int

    @override
    def evaluate(self, part: Part) -> bool:
        return part.values[self.variable] < self.number

    @override
    def split(self, part_range: Parts) -> tuple[Parts | None, Parts | None]:
        accepted, rejected = part_range.split(self.variable, self.number)
        return (accepted, rejected)


@frozen
class GreaterThan(Condition):
    variable: str
    number: int

    @override
    def evaluate(self, part: Part) -> bool:
        return part.values[self.variable] > self.number

    @override
    def split(self, part_range: Parts) -> tuple[Parts | None, Parts | None]:
        rejected, accepted = part_range.split(self.variable, self.number + 1)
        return (accepted, rejected)


@frozen
class Rule:
    condition: Condition
    destination: str

    @staticmethod
    def from_text(text: str) -> Rule:
        parts = text.split(":")
        destination = parts[-1]
        condition_text = "" if len(parts) == 1 else parts[0]
        condition = Condition.from_text(condition_text)
        return Rule(condition, destination)


@frozen
class Workflow:
    name: str
    rules: list[Rule]

    @staticmethod
    def from_text(text: str) -> Workflow:
        name, text_rules = text.split("{")  # }
        text_rules = text_rules[:-1]
        rules = [Rule.from_text(rule) for rule in text_rules.split(",")]
        return Workflow(name, rules)


def accepted(workflows: dict[str, Workflow], part: Part) -> bool:
    workflow = workflows["in"]
    while True:
        for rule in workflow.rules:
            if rule.condition.evaluate(part):
                destination = rule.destination
                if destination == "A":
                    return True
                if destination == "R":
                    return False
                workflow = workflows[destination]
                break
        else:
            raise AssertionError


def accepted_volume(workflows: dict[str, Workflow], start: Parts) -> int:
    volume = 0
    stack = [("in", start)]

    while stack:
        destination, parts = stack.pop()

        if destination == "R":
            continue

        if destination == "A":
            volume += parts.volume()
            continue

        workflow = workflows[destination]
        for rule in workflow.rules:
            accepted, rejected = rule.condition.split(parts)
            if accepted is not None:
                stack.append((rule.destination, accepted))
            if rejected is None:
                break
            parts = rejected
        else:
            raise AssertionError

    return volume


def solve() -> None:
    puzzle = data_dir() / "day19.txt"
    data = puzzle.read_text(encoding="utf-8")
    lines = data.splitlines()

    sections = (
        list(section) for key, section in itertools.groupby(lines, key=bool) if key
    )
    workflows = [Workflow.from_text(line) for line in next(sections)]
    workflow_map = {w.name: w for w in workflows}
    parts = [Part.from_text(line) for line in next(sections)]

    part_one = sum(part.rating() for part in parts if accepted(workflow_map, part))
    print(f"Part one: {part_one}")

    ranges = {var: Range(1, 4001) for var in "xmas"}
    start = Parts(ranges)
    part_two = accepted_volume(workflow_map, start)
    print(f"Part two: {part_two}")
