import sys
from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Tuple
from uuid import uuid4

import pandas as pd


@dataclass
class TennisPlayer:
    name: str = None


@dataclass
class TennisSet:
    id: int
    date: date = date.today()
    scores: Tuple = (0, 0)

    def __post_init__(self):
        self.update()

    def update(self):
        if max(self.scores) >= 6 and max(self.scores) - min(self.scores) >= 2:
            self.status = "Complete"
            self.winner = self.scores.index(max(self.scores))
        else:
            self.status = "In Progress"
            self.winner = None

    def set_score(self, scores: Tuple = (0, 0)):
        # No negative scores
        if min(scores) < 0:
            raise ValueError("Scores cannot be negative")
        # For sets higher tha 6 points the difference cant be more than 2
        if (max(scores) > 6) and (max(scores) - min(scores) > 2):
            raise ValueError("Not a valid score")

        self.scores = scores
        self.update()


@dataclass
class TennisMatch:
    id: str = uuid4().hex
    players: Tuple = (TennisPlayer(), TennisPlayer())
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    def __post_init__(self):
        self.sets = list()
        self.status = "In Progress"

    def update(self):
        if len(self.sets) == 0:
            self.status = "In Progress"
            self.winner = None
            self.sets_won = (0, 0)
            return
        if len(self.sets) > 3:
            raise ValueError("Match cannot have more than 3 sets")

        self.start_date = self.sets[0].date

        player1_wins = sum([1 for set in self.sets if set.winner == 0])
        player2_wins = sum([1 for set in self.sets if set.winner == 1])

        if player1_wins > 2 or player2_wins > 2:
            raise ValueError("Match cannot have more than 2 sets won by a player")

        if player1_wins == 2:
            self.status = "Complete"
            self.winner = self.players[0]
            self.end_date = self.sets[-1].date
            return
        if player2_wins == 2:
            self.status = "Complete"
            self.winner = self.players[1]
            self.end_date = self.sets[-1].date
            return

        self.status = "In Progress"
        self.winner = None
        self.sets_won = (player1_wins, player2_wins)
        return

    def new_set(self, scores: Tuple = (0, 0)):
        if self.status == "Complete":
            raise ValueError("Match is complete")
        if len(self.sets) == 0 or self.sets[-1].status == "Complete":
            set = TennisSet(id=len(self.sets) + 1, scores=scores)
            self.sets.append(set)
            self.update()
        else:
            raise ValueError("Current set is not complete")

    def update_scores(self, scores: Tuple = (0, 0)):
        # if self.status == "Complete":
        #     raise ValueError("Match is complete")
        # if self.sets[-1].status == "Complete":
        #     raise ValueError("Current set is complete")
        self.sets[-1].set_score(scores)
        self.update()

    def increment_game(self, player: int, amount: int = 1):
        scores = list(self.sets[-1].scores)
        scores[player] += amount
        self.update_scores(tuple(scores))

    def to_series(self):
        return pd.Series(self.__dict__)

    def scoreboard(self):
        records = []
        for i in range(len(self.players)):
            record = dict()
            record["name"] = self.players[i].name
            record["games"] = [set.scores[i] for set in self.sets]
            records.append(record)

        return pd.DataFrame(records).set_index("name")


if __name__ == "__main__":
    pass
