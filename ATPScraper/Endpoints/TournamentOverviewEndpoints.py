# flask dependencies
from flask_restful import Resource
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser

# scraper dependencies
from scraper.TournamentOverviewParser import ParseTournametOverViewPage
from scraper.Parser import parse_player_name


# Endpoints
class TournamentOverview(Resource):
    def get(self, name):
        name = parse_player_name(name)
        tournament = ParseTournametOverViewPage(name)
        return {'tournament': [{'name': name, 'overview': tournament()}]}
