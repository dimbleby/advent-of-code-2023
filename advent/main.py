#!/usr/bin/env python3
from __future__ import annotations

import importlib
import sys


def solve(day: int) -> None:
    try:
        module = importlib.import_module(f"advent.day{day:02}")
        module.solve()
    except ModuleNotFoundError:
        print(f"Day {day} not implemented")


def main() -> None:
    day = int(sys.argv[1])
    solve(day)


if __name__ == "__main__":
    for day in range(1, 26):
        print(f"Day {day}:")
        solve(day)
        print()
