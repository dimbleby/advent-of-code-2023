#!/usr/bin/env python3
from __future__ import annotations

import importlib
import sys


def main() -> None:
    day = int(sys.argv[1])
    try:
        module = importlib.import_module(f"advent.day{day:02}")
        module.solve()
    except ModuleNotFoundError:
        print(f"Day {day} not implemented")


if __name__ == "__main__":
    main()
