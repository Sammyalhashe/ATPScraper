# flask dependencies
from flask_restful import Resource

# scraper dependencies
from scraper.Parser import get_top_10



class GetTopTen(Resource):
    def get(self):
        top_10 = get_top_10()
        return {'top_10': top_10}


