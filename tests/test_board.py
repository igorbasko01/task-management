import unittest

from task_cli.board import Board


class BoardTests(unittest.TestCase):
    def test_board_equals_name_str_returns_true(self):
        self.assertTrue(Board("Test Board", "TB") == "Test Board")
    
    def test_board_equals_acronym_str_returns_true(self):
        self.assertTrue(Board("Test Board", "TB") == "TB")

    def test_board_equals_name_returns_false(self):
        self.assertFalse(Board("Test Board", "TB") == "Other Board")

    def test_board_equals_name_str_case_insensitive_returns_true(self):
        self.assertTrue(Board("Test Board", "TB") == "test board")

    def test_board_equals_acronym_str_case_insensitive_returns_true(self):
        self.assertTrue(Board("Test Board", "TB") == "tb")

    def test_board_str(self):
        self.assertEqual(str(Board("Test Board", "TB")), "Test Board (TB)")

    def test_board_from_allowed_boards(self):
        board = Board.from_allowed_boards("In Progress", 
                                          allowed_boards=[Board("In Progress", "IP"), Board("Done", "DN")])
        self.assertEqual(board, Board("In Progress", "IP"))