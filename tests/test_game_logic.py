import unittest
from unittest.mock import patch
from main import NomicGame

class TestNomicGame(unittest.TestCase):

    def setUp(self):
        self.game = NomicGame()

    @patch('main.random.randint')
    def test_roll_die(self, mock_randint):
        mock_randint.return_value = 4
        result = self.game.roll_die()
        self.assertEqual(result, 4)

    def test_conduct_vote(self):
        self.game.players = ['Alice', 'Bob']
        with patch('main.input', side_effect=['y', 'n']):
            result = self.game.conduct_vote('Test Proposal')
            self.assertFalse(result)

    @patch('main.NomicGame.roll_die')
    @patch('main.NomicGame.conduct_vote')
    def test_take_turn(self, mock_conduct_vote, mock_roll_die):
        mock_roll_die.return_value = 5
        mock_conduct_vote.return_value = True
        self.game.players = ['Alice']
        self.game.take_turn()
        mock_roll_die.assert_called_once()
        mock_conduct_vote.assert_called_once_with('Player Alice rolled a 5. Does the rule apply?')

if __name__ == '__main__':
    unittest.main()