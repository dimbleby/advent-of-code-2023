from __future__ import annotations

from dataclasses import dataclass

from advent.utils import data_dir


@dataclass(frozen=True)
class Card:
    number: int
    winners: set[int]
    mine: set[int]

    @staticmethod
    def from_string(string: str) -> Card:
        header, body = string.split(": ")
        _card, number = header.split()
        winners, mine = body.split("| ")
        ws = {int(w) for w in winners.split()}
        ms = {int(m) for m in mine.split()}
        return Card(int(number), ws, ms)

    def matches(self) -> int:
        matches = self.winners & self.mine
        return len(matches)

    def score(self) -> int:
        matches = self.matches()
        score: int = 0 if matches == 0 else 2 ** (matches - 1)
        return score


def solve() -> None:
    puzzle = data_dir() / "day04.txt"
    data = puzzle.read_text(encoding="utf-8")
    lines = data.splitlines()
    cards = [Card.from_string(line) for line in lines]

    part_one = sum(card.score() for card in cards)
    print(f"Part one: {part_one}")

    counts = {card.number: 1 for card in cards}
    for card in cards:
        count = counts[card.number]
        matches = card.matches()
        for n in range(card.number + 1, card.number + matches + 1):
            if n > len(cards):
                continue
            counts[n] += count

    part_two = sum(counts.values())
    print(f"Part two: {part_two}")
