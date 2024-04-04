import unittest
from unittest.mock import patch
from nomic_game import NomicGame

class TestNomicGame(unittest.TestCase):

    def setUp(self):
        self.game = NomicGame()

    @patch('nomic_game.SomeExternalDependency')
    def test_initialize_game(self, mock_dependency):
        self.game.initialize_game()
        self.assertTrue(self.game.is_initialized)

    @patch('nomic_game.SomeExternalDependency')
    def test_add_player(self, mock_dependency):
        player_name = 'Alice'
        self.game.add_player(player_name)
        self.assertIn(player_name, self.game.players)

    @patch('nomic_game.SomeExternalDependency')
    def test_remove_player(self, mock_dependency):
        player_name = 'Bob'
        self.game.add_player(player_name)
        self.game.remove_player(player_name)
        self.assertNotIn(player_name, self.game.players)

    @patch('nomic_game.SomeExternalDependency')
    def test_start_game(self, mock_dependency):
        self.game.start_game()
        self.assertTrue(self.game.is_game_started)

    @patch('nomic_game.SomeExternalDependency')
    def test_end_game(self, mock_dependency):
        self.game.end_game()
        self.assertFalse(self.game.is_game_started)

if __name__ == '__main__':
    unittest.main()
