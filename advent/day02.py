from __future__ import annotations

from attrs import frozen

from advent.utils import data_dir


@frozen
class Cubes:
    red: int
    green: int
    blue: int

    @staticmethod
    def from_string(string: str) -> Cubes:
        red = green = blue = 0
        parts = string.split(", ")

        for part in parts:
            number, colour = part.split()
            count = int(number)
            match colour:
                case "red":
                    red = count
                case "green":
                    green = count
                case "blue":
                    blue = count
                case other:
                    message = f"unexpected colour {other}"
                    raise AssertionError(message)

        return Cubes(red, green, blue)

    def possible(self, maximum: Cubes) -> bool:
        return (
            self.red <= maximum.red
            and self.green <= maximum.green
            and self.blue <= maximum.blue
        )

    def power(self) -> int:
        return self.red * self.green * self.blue


@frozen
class Game:
    number: int
    rounds: list[Cubes]

    @staticmethod
    def from_string(string: str) -> Game:
        header, body = string.split(": ")
        _game, number = header.split()
        rounds = [Cubes.from_string(round_) for round_ in body.split("; ")]
        return Game(int(number), rounds)

    def possible(self, maximum: Cubes) -> bool:
        return all(round_.possible(maximum) for round_ in self.rounds)

    def minimum(self) -> Cubes:
        red = max(round_.red for round_ in self.rounds)
        green = max(round_.green for round_ in self.rounds)
        blue = max(round_.blue for round_ in self.rounds)
        return Cubes(red, green, blue)


def solve() -> None:
    puzzle = data_dir() / "day02.txt"
    data = puzzle.read_text(encoding="utf-8")
    lines = data.splitlines()
    games = [Game.from_string(line) for line in lines]

    maximum = Cubes(red=12, green=13, blue=14)
    part_one = sum(game.number for game in games if game.possible(maximum))
    print(f"Part one: {part_one}")

    part_two = sum(game.minimum().power() for game in games)
    print(f"Part two: {part_two}")
