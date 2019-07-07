# flask dependencies
from flask_restful import Resource

# scraper dependencies
from scraper.PlayerPageParser import parse_player_page

# Utils
def parse_player(player):
    return {
        'player': {
            'name': player.name,
            'bio': player.bio,
            'current_year_stats': player.cy_stats,
            'career_stats': player.career_stats
        }
    }

# Endpoints
class PlayerOverview(Resource):
    def get(self, name):
        player = parse_player_page(name)
        player_parsed = parse_player(player)
        return {'player': {
            'name': name,
            'ranking_history': player_parsed
        }}
