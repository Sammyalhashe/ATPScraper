# flask dependencies
from flask_restful import Resource
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser

# scraper dependencies
from scraper.PlayerRankingsBreakdownParser import parse_player_ranking_breakdown
from scraper.Parser import parse_player_name


# Endpoints
class PlayerRankingsBreakdown(Resource):
    """PlayerRankingsBreakdown
    should add doubles option also
    """
    def get(self, name):
        name = parse_player_name(name)
        return parse_player_ranking_breakdown(name)
