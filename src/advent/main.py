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
    if len(sys.argv) < 2:
        for day in range(1, 26):
            print(f"Part {day}:")
            solve(day)
            print()

    else:
        day = int(sys.argv[1])
        solve(day)


if __name__ == "__main__":
    main()
