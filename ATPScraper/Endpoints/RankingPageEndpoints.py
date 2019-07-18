# flask dependencies
from flask_restful import Resource

# scraper dependencies
from scraper.Parser import get_top_10



class GetTopTen(Resource):
    """GetTopTen"""
    def get(self):
        """get

        /api/top_10

        """
        top_10 = get_top_10()
        return {'top_10': top_10}


