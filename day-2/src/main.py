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

    def guess_move(self):
        match self.outcome:
            case RPSOutcome.DRAW:
                self.get_drawing_move()
            case RPSOutcome.WIN:
                self.get_winning_move()
            case RPSOutcome.LOSE:
                self.get_losing_move()

    def get_drawing_move(self):
        self.your_move = self.opponent_move

    def get_winning_move(self):
        match self.opponent_move:
            case RPSState.PAPER:
                self.your_move = RPSState.SCISSORS
            case RPSState.ROCK:
                self.your_move = RPSState.PAPER
            case RPSState.SCISSORS:
                self.your_move = RPSState.ROCK

    def get_losing_move(self):
        match self.opponent_move:
            case RPSState.PAPER:
                self.your_move = RPSState.ROCK
            case RPSState.ROCK:
                self.your_move = RPSState.SCISSORS
            case RPSState.SCISSORS:
                self.your_move = RPSState.PAPER

    def calculate_score(self):
        return self.your_move.value + self.outcome.value


class RPSParser:
    def __init__(self, file: Path):
        self.moves: list[RPSMoveStrategy] = []
        self.raw_entries = file.read_text().splitlines(False)

    def feed(self):
        for entry in self.raw_entries:
            opponent, outcome = list(map(self.parse_code, entry.split()))
            strategy = RPSMoveStrategy(opponent, None, outcome)

            strategy.guess_move()

            self.moves.append(strategy)

    def parse_code(self, item: str) -> RPSState:
        match item:
            case "A":
                return RPSState.ROCK
            case "B":
                return RPSState.PAPER
            case "C":
                return RPSState.SCISSORS
            case "X":
                return RPSOutcome.LOSE
            case "Y":
                return RPSOutcome.DRAW
            case "Z":
                return RPSOutcome.WIN

    def calculate_player_scores(self):
        return sum((move.calculate_score() for move in self.moves))


if __name__ == "__main__":
    parser = RPSParser(Path("day-2/input.txt"))

    parser.feed()
    print(parser.calculate_player_scores())
