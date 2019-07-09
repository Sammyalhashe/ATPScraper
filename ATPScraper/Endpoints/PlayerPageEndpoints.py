# flask dependencies
from flask_restful import Resource
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser

# scraper dependencies
from scraper.PlayerPageParser import parse_player_page, get_player_rank


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
    def get(self, name):
        player = parse_player_page(name)
        player_parsed = parse_player(player)
        return {'player': {'name': name, 'ranking_history': player_parsed}}

class PlayerRanking(Resource):
    args = {
        'singles': fields.Bool(missing=True)
    }
    
    @use_kwargs(args)
    def get(self, name, singles=True):
        rank = get_player_rank(name, singles)
        return {'player': {'name': name, 'rank': rank}}
