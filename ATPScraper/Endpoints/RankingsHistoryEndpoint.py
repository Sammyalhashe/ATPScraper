# flask dependencies
from flask_restful import Resource

# scraper dependencies
from scraper.PlayerRankingHistoryParser import get_player_ranking_history

# Utils
def parse_ranking(ranking):
    return {
        'date': ranking.date,
        'singles': ranking.singles,
        'doubles': ranking.doubles
    }

# Endpoints
class RankingHistory(Resource):
    def get(self, name):
        ranking_hist = get_player_ranking_history(name)
        ranking_hist_parsed = list(map(lambda x: parse_ranking(x), ranking_hist))
        return {'player': {
            'name': name,
            'ranking_history': ranking_hist_parsed
        }}
