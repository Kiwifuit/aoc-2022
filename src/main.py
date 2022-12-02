from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Elf:
    calories: list[int]
    calories_total: int


def get_all_elves():
    raw = Path("day-1/input.txt").read_text().split("\n\n")

    for elf in raw:
        calories = list(map(int, elf.splitlines(False)))
        total = sum(calories)

        yield Elf(calories, total)


def calculate_top_n(population: list[int], limit: int):
    res = []

    for _ in range(limit):
        biggest = max(population)
        res.append(biggest)
        population.remove(biggest)

    return res


if __name__ == "__main__":
    calories_totals = [elf.calories_total for elf in get_all_elves()]
    top_three_elves = calculate_top_n(calories_totals, 3)

    print(sum(top_three_elves))
