"""Test for SSAppV1"""
import unittest
from unittest.mock import patch
from datetime import datetime
from src.app_v1 import SSApp, NotEnoughPlayersException

class SSAppV1(unittest.TestCase):
    """Test of SecreteSantaApp"""

    def setUp(self) -> None:
        """Setup for SSAppV1"""

        self.game = SSApp()
        self.mock_events = {
            "missing_players": {
                "name": "Christmas",
                "date_time": datetime.now(),
                "participants": [],
                "location": "Home",
            },
            "missing_location": {
                "name": "Christmas",
                "date_time": datetime.now(),
                "participants": ["A", "B", "C", "D"],
            },
            "empty_location": {
                "name": "Christmas",
                "date_time": datetime.now(),
                "participants": ["A", "B", "C", "D"],
                "location": "",
            },
            "one_players": {
                "name": "Christmas",
                "date_time": datetime.now(),
                "participants": ["A"],
                "location": "Home",
            },
            "two_players": {
                "name": "Christmas",
                "date_time": datetime.now(),
                "participants": ["A", "B"],
                "location": "Office",
            },
            "odd_player": {
                "name": "Christmas",
                "date_time": datetime.now(),
                "participants": ["A", "B", "C"],
                "location": "Home",
            },
            "even_player": {
                "name": "Christmas",
                "date_time": datetime.now(),
                "participants": ["A", "B", "C", "D"],
                "location": "Home",
            },
        }
        return super().setUp()

    def test_not_enough_player_exceptions_case(self):
        """Not enough player exception case"""
        with self.assertRaises(NotEnoughPlayersException):
            self.game.create_event(**self.mock_events["missing_players"])

        with self.assertRaises(NotEnoughPlayersException):
            self.game.create_event(**self.mock_events["one_players"])

        res = self.game.create_event(**self.mock_events["two_players"])
        self.assertEqual(str, type(res))
        self.assertEqual(
            self.mock_events["two_players"]["name"],
            self.game.get_event_info(res).event_name
        )

    def test_missing_location_case(self):
        """Missing Location Case"""
        res = self.game.create_event(**self.mock_events["missing_location"])
        self.assertEqual(str, type(res))
        self.assertEqual(
            self.mock_events["missing_location"]["name"],
            self.game.get_event_info(res).event_name,
        )
        self.assertEqual(
            self.mock_events["missing_location"]["date_time"],
            self.game.get_event_info(res).event_date_time,
        )
        self.assertEqual(
            self.mock_events["missing_location"]["participants"],
            self.game.get_event_info(res).event_participants,
        )
        self.assertEqual(
            "",
            self.game.get_event_info(res).event_location,
        )

    def test_empty_create_location_case(self):
        """Empty Location Case"""
        res = self.game.create_event(**self.mock_events["empty_location"])
        self.assertEqual(str, type(res))
        self.assertEqual(
            self.mock_events["empty_location"]["name"],
            self.game.get_event_info(res).event_name,
        )
        self.assertEqual(
            self.mock_events["empty_location"]["date_time"],
            self.game.get_event_info(res).event_date_time,
        )
        self.assertEqual(
            self.mock_events["empty_location"]["participants"],
            self.game.get_event_info(res).event_participants,
        )
        self.assertEqual(
            self.mock_events["empty_location"]["location"],
            self.game.get_event_info(res).event_location,
        )

    @patch("src.app_v1.random")
    def test_odd_player_case(self, mock_random):
        """Odd Player Case"""
        mock_random.choice.side_effect = ["B", "C", "A"]
        exp_odd_map = {"A": "B", "B":"C", "C":"A"}
        res = self.game.create_event(**self.mock_events["odd_player"])
        self.assertEqual(str, type(res))
        self.assertEqual(
            self.mock_events["odd_player"]["name"],
            self.game.get_event_info(res).event_name,
        )
        self.assertEqual(
            self.mock_events["odd_player"]["date_time"],
            self.game.get_event_info(res).event_date_time,
        )
        self.assertEqual(
            self.mock_events["odd_player"]["participants"],
            self.game.get_event_info(res).event_participants,
        )
        self.assertEqual(
            self.mock_events["odd_player"]["location"],
            self.game.get_event_info(res).event_location,
        )
        self.assertEqual(
            len(exp_odd_map),
            len(self.game.get_event_info(res).event_santa_map),
        )

        self.assertDictEqual(
            exp_odd_map,
            self.game.get_event_info(res).event_santa_map,
        )

    @patch("src.app_v1.random")
    def test_odd_player_with_out_of_choices_case(self, mock_random):
        """Odd Player with out of choices Case"""
        mock_random.choice.side_effect = ["B", "A", "A"]
        exp_odd_map = {"A": "C", "B":"A", "C":"B"}
        res = self.game.create_event(**self.mock_events["odd_player"])
        self.assertEqual(str, type(res))
        self.assertEqual(
            self.mock_events["odd_player"]["name"],
            self.game.get_event_info(res).event_name,
        )
        self.assertEqual(
            self.mock_events["odd_player"]["date_time"],
            self.game.get_event_info(res).event_date_time,
        )
        self.assertEqual(
            self.mock_events["odd_player"]["participants"],
            self.game.get_event_info(res).event_participants,
        )
        self.assertEqual(
            self.mock_events["odd_player"]["location"],
            self.game.get_event_info(res).event_location,
        )
        self.assertEqual(
            len(exp_odd_map),
            len(self.game.get_event_info(res).event_santa_map),
        )

        self.assertDictEqual(
            exp_odd_map,
            self.game.get_event_info(res).event_santa_map,
        )

    @patch("src.app_v1.random")
    def test_even_player(self, mock_random):
        """Even Player Case"""
        mock_random.choice.side_effect = ["B", "A", "D", "C"]
        exp_odd_map = {"A": "B", "B":"A", "C":"D", "D":"C"}
        res = self.game.create_event(**self.mock_events["even_player"])
        self.assertEqual(str, type(res))
        self.assertEqual(
            self.mock_events["even_player"]["name"],
            self.game.get_event_info(res).event_name,
        )
        self.assertEqual(
            self.mock_events["even_player"]["date_time"],
            self.game.get_event_info(res).event_date_time,
        )
        self.assertEqual(
            self.mock_events["even_player"]["participants"],
            self.game.get_event_info(res).event_participants,
        )
        self.assertEqual(
            self.mock_events["even_player"]["location"],
            self.game.get_event_info(res).event_location,
        )
        self.assertEqual(
            len(exp_odd_map),
            len(self.game.get_event_info(res).event_santa_map),
        )

        self.assertDictEqual(
            exp_odd_map,
            self.game.get_event_info(res).event_santa_map,
        )

    def test_cancel_events(self):
        """Cancel Event method"""
        res = self.game.create_event(**self.mock_events["even_player"])

        self.assertEqual(str, type(res))
        self.game.cancel_event(res)
        self.assertIsNone(self.game.get_event_info(res))


if __name__ == "__main__":
    unittest.main()
