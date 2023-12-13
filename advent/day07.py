from __future__ import annotations

from collections import Counter

from attrs import frozen

from advent.utils import data_dir

VALUES = {str(n): n for n in range(2, 10)} | {
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}

VALUES2 = {str(n): n for n in range(2, 10)} | {
    "T": 10,
    "J": 1,
    "Q": 12,
    "K": 13,
    "A": 14,
}


class Kind:
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


def classify(counts: list[int]) -> int:
    if counts[0] == 5:
        return Kind.FIVE_OF_A_KIND
    if counts[0] == 4:
        return Kind.FOUR_OF_A_KIND
    if counts[0] == 3 and counts[1] == 2:
        return Kind.FULL_HOUSE
    if counts[0] == 3:
        return Kind.THREE_OF_A_KIND
    if counts[0] == 2 and counts[1] == 2:
        return Kind.TWO_PAIR
    if counts[0] == 2:
        return Kind.ONE_PAIR

    return Kind.HIGH_CARD


@frozen
class Hand:
    values: list[int]

    def kind(self) -> int:
        counter = Counter(self.values)
        weak_jacks = counter.pop(1, 0)
        counts = sorted(counter.values(), reverse=True) or [0]
        counts[0] += weak_jacks
        return classify(counts)


@frozen
class Play:
    hand: Hand
    bid: int

    @staticmethod
    def from_string(string: str, part_two: bool = False) -> Play:
        table = VALUES2 if part_two else VALUES
        faces, bid = string.split()
        values = [table[face] for face in faces]
        hand = Hand(values)
        return Play(hand, int(bid))


def solve() -> None:
    puzzle = data_dir() / "day07.txt"
    data = puzzle.read_text(encoding="utf-8")

    plays = [Play.from_string(string) for string in data.splitlines()]
    plays = sorted(plays, key=lambda play: (play.hand.kind(), play.hand.values))
    part_one = sum(index * play.bid for index, play in enumerate(plays, 1))
    print(f"Part one: {part_one}")

    plays = [Play.from_string(string, part_two=True) for string in data.splitlines()]
    plays = sorted(plays, key=lambda play: (play.hand.kind(), play.hand.values))
    part_two = sum(index * play.bid for index, play in enumerate(plays, 1))
    print(f"Part two: {part_two}")
