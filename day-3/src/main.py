from dataclasses import dataclass
from pathlib import Path
from enum import Enum


class Item(Enum):
    LOWERCASE_A = "a"
    LOWERCASE_B = "b"
    LOWERCASE_C = "c"
    LOWERCASE_D = "d"
    LOWERCASE_E = "e"
    LOWERCASE_F = "f"
    LOWERCASE_G = "g"
    LOWERCASE_H = "h"
    LOWERCASE_I = "i"
    LOWERCASE_J = "j"
    LOWERCASE_K = "k"
    LOWERCASE_L = "l"
    LOWERCASE_M = "m"
    LOWERCASE_N = "n"
    LOWERCASE_O = "o"
    LOWERCASE_P = "p"
    LOWERCASE_Q = "q"
    LOWERCASE_R = "r"
    LOWERCASE_S = "s"
    LOWERCASE_T = "t"
    LOWERCASE_U = "u"
    LOWERCASE_V = "v"
    LOWERCASE_W = "w"
    LOWERCASE_X = "x"
    LOWERCASE_Y = "y"
    LOWERCASE_Z = "z"
    UPPERCASE_A = "A"
    UPPERCASE_B = "B"
    UPPERCASE_C = "C"
    UPPERCASE_D = "D"
    UPPERCASE_E = "E"
    UPPERCASE_F = "F"
    UPPERCASE_G = "G"
    UPPERCASE_H = "H"
    UPPERCASE_I = "I"
    UPPERCASE_J = "J"
    UPPERCASE_K = "K"
    UPPERCASE_L = "L"
    UPPERCASE_M = "M"
    UPPERCASE_N = "N"
    UPPERCASE_O = "O"
    UPPERCASE_P = "P"
    UPPERCASE_Q = "Q"
    UPPERCASE_R = "R"
    UPPERCASE_S = "S"
    UPPERCASE_T = "T"
    UPPERCASE_U = "U"
    UPPERCASE_V = "V"
    UPPERCASE_W = "W"
    UPPERCASE_X = "X"
    UPPERCASE_Y = "Y"
    UPPERCASE_Z = "Z"

    @property
    def priority(self) -> int:
        return list(Item).index(self) + 1


@dataclass(repr=False)
class RucksackCompartment:
    id: int
    items: list[Item]
    length: int

    def __repr__(self):
        return f"""<Compartment #{self.id}'s items: {"".join(map(lambda i: i.value, self.items))!r}>"""


@dataclass()
class Rucksack:
    compartments: list[RucksackCompartment]
    all: str

    def build_compartments(self):
        cut_index = len(self.all) // 2

        self.compartments = [
            RucksackCompartment(
                compartment_id,
                list(map(Item, compartment)),
                len(compartment),
            )
            for compartment_id, compartment in enumerate(
                (self.all[:cut_index], self.all[cut_index:]), start=1
            )
        ]

    def find_common(self) -> Item:
        compartments = self.compartments

        return list(
            set(filter(lambda item: item in compartments[1].items, compartments[0].items))
        )[0]

    @property
    def all_items(self):
        for compartment in self.compartments:
            yield from compartment.items


@dataclass(frozen=True)
class ElfGroup:
    rucksacks: tuple[Rucksack, Rucksack, Rucksack]

    def find_badge(self):
        all_items = [list(rucksack.all_items) for rucksack in self.rucksacks]

        for item in all_items:
            return list(
                set(
                    filter(
                        lambda item: item in all_items[1] and item in all_items[2], item
                    )
                )
            )[0]


def get_elf_groups() -> list[ElfGroup]:
    raw = Path("day-3/input.txt").read_text().splitlines()

    rucksack_storage = []
    for counter, line in enumerate(raw, 1):
        rucksack = Rucksack(None, line)

        rucksack.build_compartments()
        rucksack_storage.append(rucksack)

        if counter % 3 == 0:
            yield ElfGroup(rucksack_storage)
            rucksack_storage.clear()


if __name__ == "__main__":
    res = sum(elf_group.find_badge().priority for elf_group in get_elf_groups())

    print(res)
