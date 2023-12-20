from __future__ import annotations

import math
from abc import ABC, abstractmethod, abstractproperty
from collections import deque

from attrs import define, field, frozen
from typing_extensions import override

from advent.utils import data_dir


@frozen
class Pulse:
    source: str
    destination: str
    value: bool


class Module(ABC):
    @staticmethod
    def from_text(text: str) -> Module:
        module, rest = text.split(" -> ")
        destinations = rest.split(", ")
        if module == "broadcaster":
            return Broadcaster(module, destinations)
        if module.startswith("%"):
            return FlipFlop(module[1:], destinations)
        if module.startswith("&"):
            return Conjunction(module[1:], destinations)
        raise AssertionError

    @abstractproperty
    def name(self) -> str:
        ...

    @abstractproperty
    def destinations(self) -> list[str]:
        ...

    @abstractmethod
    def react(self, pulse: Pulse) -> list[Pulse]:
        ...


@define
class Broadcaster(Module):
    name: str
    destinations: list[str]

    @override
    def react(self, pulse: Pulse) -> list[Pulse]:
        return [
            Pulse(self.name, destination, pulse.value)
            for destination in self.destinations
        ]


@define
class FlipFlop(Module):
    name: str
    destinations: list[str]
    state: bool = False

    @override
    def react(self, pulse: Pulse) -> list[Pulse]:
        if pulse.value:
            return []

        self.state = not self.state
        return [
            Pulse(self.name, destination, self.state)
            for destination in self.destinations
        ]


@define
class Conjunction(Module):
    name: str
    destinations: list[str]
    inputs: dict[str, bool] = field(factory=dict)

    @override
    def react(self, pulse: Pulse) -> list[Pulse]:
        self.inputs[pulse.source] = pulse.value
        output = not all(self.inputs.values())
        return [
            Pulse(self.name, destination, output) for destination in self.destinations
        ]


def solve() -> None:
    puzzle = data_dir() / "day20.txt"
    data = puzzle.read_text(encoding="utf-8")

    module_list = [Module.from_text(line) for line in data.splitlines()]
    modules = {module.name: module for module in module_list}
    for module in module_list:
        for destination in module.destinations:
            dest_module = modules.get(destination)
            if isinstance(dest_module, Conjunction):
                dest_module.inputs[module.name] = False

    button_counter = 0
    low_pulses = 0
    high_pulses = 0

    # There is a conjunction pointing at rx, we need all four of its inputs to be high.
    rx_input = next(module for module in module_list if "rx" in module.destinations)
    rx_input_cycles: dict[str, int] = {}

    while len(rx_input_cycles) < 4:
        if button_counter == 1000:
            part_one = low_pulses * high_pulses

        button_counter += 1

        queue = deque([Pulse("button", "broadcaster", False)])
        while queue:
            pulse = queue.popleft()
            if pulse.value:
                high_pulses += 1
            else:
                low_pulses += 1

            if pulse.destination == rx_input.name and pulse.value:
                rx_input_cycles.setdefault(pulse.source, button_counter)

            dest_module = modules.get(pulse.destination)
            if dest_module is not None:
                pulses = dest_module.react(pulse)
                queue.extend(pulses)

    print(f"Part one: {part_one}")

    part_two = math.lcm(*rx_input_cycles.values())
    print(f"Part two: {part_two}")
