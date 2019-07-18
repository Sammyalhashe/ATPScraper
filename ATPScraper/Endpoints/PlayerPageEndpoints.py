# flask dependencies
from flask_restful import Resource
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser

# scraper dependencies
from scraper.PlayerPageParser import parse_player_page, get_player_rank
from scraper.Parser import parse_player_name


# Utils
def parse_player(player):
    return {} if not player else {
        'player': {
            'name': player.name,
            'bio': player.bio,
            'current_year_stats': player.cy_stats,
            'career_stats': player.career_stats,
            'fundamentals': player.fundamentals
        }
    }


# Endpoints
class PlayerOverview(Resource):
    """PlayerOverview"""

    def get(self, name):
        """get

        /api/player_overview/{name}

        :param name: name of the player
        """
        name = parse_player_name(name)
        player = parse_player_page(name)
        player_parsed = parse_player(player)
        return {'player': [{'name': name, 'stats': player_parsed}]}


class PlayerRanking(Resource):
    """PlayerRanking"""
    # https://webargs.readthedocs.io/en/latest/quickstart.html#basic-usage
    args = {'singles': fields.Bool(missing=True)}

    @use_kwargs(args)
    def get(self, name, singles=True):
        """get

        /api/player_ranking/{name}

        :param name: name of the player
        :param singles: singles or doubles?
        """
        name = parse_player_name(name)
        rank = get_player_rank(name, singles)
        return {'player': [{'name': name, 'rank': rank}]}
