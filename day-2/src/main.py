from dataclasses import dataclass
from pathlib import Path
from enum import Enum


class RPSState(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class RPSOutcome(Enum):
    LOSE = 0
    DRAW = 3
    WIN = 6


@dataclass()
class RPSMoveStrategy:
    opponent_move: RPSState
    your_move: RPSState
    outcome: RPSOutcome

    def decide_condition(self):
        if self.your_move == self.opponent_move:
            self.outcome = RPSOutcome.DRAW

        match (self.your_move, self.opponent_move):
            case (RPSState.PAPER, RPSState.ROCK) | (RPSState.PAPER, RPSState.ROCK,) | (
                RPSState.SCISSORS,
                RPSState.PAPER,
            ) | (RPSState.ROCK, RPSState.SCISSORS):
                self.outcome = RPSOutcome.WIN
            case (RPSState.ROCK, RPSState.PAPER) | (RPSState.ROCK, RPSState.PAPER,) | (
                RPSState.PAPER,
                RPSState.SCISSORS,
            ) | (RPSState.SCISSORS, RPSState.ROCK):
                self.outcome = RPSOutcome.LOSE

        print(self.outcome)

    def calculate_score(self):
        return self.your_move.value + self.outcome.value


class RPSParser:
    def __init__(self, file: Path):
        self.moves: list[RPSMoveStrategy] = []
        self.raw_entries = file.read_text().splitlines(False)

    def feed(self):
        for entry in self.raw_entries:
            opponent, player = list(map(self.parse_code, entry.split()))
            strategy = RPSMoveStrategy(opponent, player, None)

            strategy.decide_condition()

            self.moves.append(strategy)

    def parse_code(self, item: str) -> RPSState:
        match item:
            case "A" | "X":
                return RPSState.ROCK
            case "B" | "Y":
                return RPSState.PAPER
            case "C" | "Z":
                return RPSState.SCISSORS

    def calculate_player_scores(self):
        return sum((move.calculate_score() for move in self.moves))


if __name__ == "__main__":
    parser = RPSParser(Path("day-2/input.txt"))

    parser.feed()
    print(parser.calculate_player_scores())
