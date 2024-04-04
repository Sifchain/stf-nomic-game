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

    def test_take_turn(self):
        with patch.object(self.game, 'roll_die', return_value=5):
            self.game.take_turn()
            self.assertEqual(self.game.current_turn, 1)

    @patch('main.input', create=True)
    def test_conduct_vote(self, mocked_input):
        mocked_input.side_effect = ['yes', 'no', 'yes']
        result = self.game.conduct_vote()
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()