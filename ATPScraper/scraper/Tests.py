from typing import List
try:
    from .Parser import *
    from .PlayerPageParser import *
    from .PlayerRankingHistoryParser import *
    from .Classes.Ranking import Ranking
    from .CacheUtils import timer
except ImportError:
    from Parser import *
    from PlayerPageParser import *
    from PlayerRankingHistoryParser import *
    from Classes.Ranking import Ranking
    from CacheUtils import timer
import unittest
john_isner = {
    'name': 'john isner',
    'bio_url': 'https://www.atptour.com/en/players/john-isner/i186/overview',
    'current_year_stats': {
        'data-singles': {
            'rank_move': -1,
            'rank': 12,
            'w-l': [15, 7],
            'titles': 0,
            'prize_money': float(997935)
        },
        'data-doubles': {
            'rank_move': 1,
            'rank': 175,
            'w-l': [2, 3],
            'titles': 0,
            'prize_money': float(39175)
        }
    },
    'career_stats': {
        'data-singles': {
            'rank': 8,
            'date_highest': '2018.07.16',
            'w-l': [409, 252],
            'titles': 14,
            'prize_money': float(17925218)
        },
        'data-doubles': {
            'rank': 26,
            'date_highest': '2012.04.02',
            'w-l': [111, 98],
            'titles': 5,
            'prize_money': float(17925218)
        }
    },
}

david_goffin = {
    'name': 'david goffin',
    'bio_url': 'https://www.atptour.com/en/players/john-isner/i186/overview',
    'current_year_stats': {
        'data-singles': {
            'rank_move': 10,
            'rank': 23,
            'w-l': [18, 15],
            'titles': 0,
            'prize_money': float(887049)
        },
        'data-doubles': {
            'rank_move': 28,
            'rank': 162,
            'w-l': [6, 4],
            'titles': 1,
            'prize_money': float(64386)
        }
    },
    'career_stats': {
        'data-singles': {
            'rank': 7,
            'date_highest': '2017.11.20',
            'w-l': [248, 159],
            'titles': 4,
            'prize_money': float(11764512)
        },
        'data-doubles': {
            'rank': 162,
            'date_highest': '2019.06.24',
            'w-l': [13, 24],
            'titles': 1,
            'prize_money': float(11764512)
        }
    },
}


class PlayerParseTest(unittest.TestCase):
    def test_playerNameParse(self):
        self.assertEqual(parse_player_name('Roger Federer'), 'roger-federer')
        self.assertEqual(parse_player_name('roger federer'), 'roger-federer')
        self.assertEqual(parse_player_name('roger Federer'), 'roger-federer')
        self.assertEqual(parse_player_name('Roger federer'), 'roger-federer')
        self.assertEqual(
            parse_player_name('   Roger federer   '), 'roger-federer')
        self.assertEqual(
            parse_player_name('   Roger    federer   '), 'roger-federer')

    def test_topTen(self):
        self.assertTrue(len(get_top_10()) == 10)

    def test_playerRank(self):
        self.assertIsInstance(get_player_rank('Rafael Nadal'), int)
        self.assertIsInstance(get_player_rank('Rafael Nadal'), int)
        self.assertIsInstance(
            get_player_rank('Rafael Nadal', singles=False), int)
        self.assertIsInstance(get_player_rank('roger federer'), int)

    def test_playerRankingHistory(self):
        self.assertIsInstance(
            get_player_ranking_history('roger federer'), List)

    def test_playerValuesTest(self):
        tennis_types = ['data-singles', 'data-doubles']
        players = [john_isner, david_goffin]

        for tennis_type, player in zip(tennis_types, players):
            # current year
            self.assertIsInstance(
                parse_player_page(
                    player['name']).cy_stats[tennis_type]['rank_move'],
                type(player['current_year_stats'][tennis_type]['rank_move']))
            self.assertIsInstance(
                parse_player_page(
                    player['name']).cy_stats[tennis_type]['rank'],
                type(player['current_year_stats'][tennis_type]['rank']))
            self.assertIsInstance(
                parse_player_page(player['name']).cy_stats[tennis_type]['w-l'],
                type(player['current_year_stats'][tennis_type]['w-l']))
            self.assertIsInstance(
                parse_player_page(
                    player['name']).cy_stats[tennis_type]['titles'],
                type(player['current_year_stats'][tennis_type]['titles']))
            self.assertIsInstance(
                parse_player_page(
                    player['name']).cy_stats[tennis_type]['prize_money'],
                type(player['current_year_stats'][tennis_type]['prize_money']))

            # career
            self.assertIsInstance(
                parse_player_page(
                    player['name']).career_stats[tennis_type]['rank'],
                type(player['career_stats'][tennis_type]['rank']))
            self.assertIsInstance(
                parse_player_page(
                    player['name']).career_stats[tennis_type]['date_highest'],
                type(player['career_stats'][tennis_type]['date_highest']))
            self.assertIsInstance(
                parse_player_page(
                    player['name']).career_stats[tennis_type]['w-l'],
                type(player['career_stats'][tennis_type]['w-l']))
            self.assertIsInstance(
                parse_player_page(
                    player['name']).career_stats[tennis_type]['titles'],
                type(player['career_stats'][tennis_type]['titles']))
            self.assertIsInstance(
                parse_player_page(
                    player['name']).career_stats[tennis_type]['prize_money'],
                type(player['career_stats'][tennis_type]['prize_money']))

    @classmethod
    def tearDownClass(cls):
        timer.cancel()


if __name__ == "__main__":
    unittest.main(verbosity=2)
