import sys
import unittest
from datetime import date

sys.path.append("..")
from datetime import date

import pandas as pd

from helpers.tennis import TennisMatch, TennisPlayer, TennisSet


class TennisPlayerTestCase(unittest.TestCase):
    def test_TennisPlayer_initialize(self):
        player = TennisPlayer(name="Alice")
        self.assertEqual(player.name, "Alice")


class TennisSetTestCase(unittest.TestCase):
    def test_TennisSet_initialize(self):
        set = TennisSet(id=1)
        today = date.today()
        self.assertEqual(set.id, 1)
        self.assertEqual(set.date, today)
        self.assertEqual(set.scores, (0, 0))
        self.assertEqual(set.status, "In Progress")
        self.assertIsNone(set.winner)

    def test_TennisSet_update(self):
        # Scores where fewer than 6 games have been won should be incomplete
        set = TennisSet(id=1)
        set.set_score((5, 4))
        self.assertEqual(set.status, "In Progress")
        self.assertEqual(set.winner, None)

        set.set_score((6, 5))
        self.assertEqual(set.status, "In Progress")
        self.assertEqual(set.winner, None)

        set.set_score((6, 4))
        self.assertEqual(set.status, "Complete")
        self.assertEqual(set.winner, 0)


class TennisMatchTestCase(unittest.TestCase):
    def test_TennisMatch_initialize(self):
        player1 = TennisPlayer(name="Alice")
        player2 = TennisPlayer(name="Bob")
        match = TennisMatch(players=(player1, player2))
        self.assertIsInstance(match.id, str)
        self.assertEqual(match.sets, list())
        match.update()
        self.assertEqual(match.status, "In Progress")
        self.assertIsNone(match.winner)

    def test_TennisMatch_new_set_raise_error(self):
        player1 = TennisPlayer(name="Alice")
        player2 = TennisPlayer(name="Bob")
        match = TennisMatch(players=(player1, player2))
        match.new_set(scores=(0, 0))

        # Adding a set when the current set is incomplete should raise an error
        self.assertEqual(match.sets[-1].status, "In Progress")
        self.assertRaises(ValueError, match.new_set, scores=(0, 0))

        match.update_scores(scores=(6, 4))
        match.new_set(scores=(6, 4))
        self.assertEqual(match.status, "Complete")
        self.assertEqual(match.winner, player1)

        # Adding a set when the match is complete should raise an error
        self.assertRaises(ValueError, match.new_set, scores=(0, 0))

    def test_TennisMatch_update_scores(self):
        player1 = TennisPlayer(name="Alice")
        player2 = TennisPlayer(name="Bob")
        match = TennisMatch(players=(player1, player2))
        match.new_set(scores=(5, 0))
        self.assertEqual(match.status, "In Progress")
        self.assertIsNone(match.winner)

        # Update score so current set is complete
        match.update_scores(scores=(6, 4))
        # Should raise error to update score after current set is complete
        self.assertEqual(match.sets[-1].status, "Complete")
        self.assertRaises(ValueError, match.update_scores, scores=(6, 4))

        # Adding a second set for player 1 to win should complete the match
        match.new_set()
        match.update_scores(scores=(6, 4))
        self.assertEqual(match.status, "Complete")
        self.assertEqual(match.winner, player1)

    def test_TennisMatch_increment_game(self):
        player1 = TennisPlayer(name="Alice")
        player2 = TennisPlayer(name="Bob")
        match = TennisMatch(players=(player1, player2))
        match.new_set(scores=(5, 0))
        match.increment_game(player=0)  # player 1 wins game
        self.assertEqual(match.sets[-1].scores, (6, 0))

        # Adding a game when the current set is complete should raise an error
        self.assertEqual(match.sets[-1].status, "Complete")
        self.assertRaises(ValueError, match.increment_game, player=0)

        # Test removing a game
        match.new_set(scores=(3, 0))
        match.increment_game(player=0, amount=-1)
        self.assertEqual(match.sets[-1].scores, (2, 0))

    def test_TennisMatch_scoreboard(self):
        player1 = TennisPlayer(name="Alice")
        player2 = TennisPlayer(name="Bob")
        match = TennisMatch(players=(player1, player2))
        match.new_set(scores=(6, 0))
        match.new_set(scores=(0, 6))
        match.new_set(scores=(6, 0))
        scoreboard = match.scoreboard()
        self.assertIsInstance(scoreboard, pd.DataFrame)
        self.assertEqual(scoreboard.shape, (2, 1))

    def test_TennisMatch_to_series(self):
        player1 = TennisPlayer(name="Alice")
        player2 = TennisPlayer(name="Bob")
        match = TennisMatch(players=(player1, player2))
        match.new_set(scores=(6, 0))
        match.new_set(scores=(0, 6))
        match.new_set(scores=(6, 0))
        out = match.to_series()
        self.assertIsInstance(out, pd.Series)
        self.assertEqual(out["id"], match.id)
        self.assertEqual(out["status"], match.status)
        self.assertEqual(out["winner"], match.winner)


if __name__ == "__main__":
    unittest.main()
