# flask dependencies
from flask_restful import Resource
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser

# scraper dependencies
from scraper.TournamentOverviewParser import ParseTournametOverViewPage, parse_from_tournament_bio_fragment
from scraper.Parser import parse_player_name


# Endpoints
class TournamentOverview(Resource):

    args = {'url': fields.Bool(missing=False)}

    @use_kwargs(args)
    def get(self, name, url):
        name = parse_player_name(name)

        if not url:
            tournament = ParseTournametOverViewPage(name)
        else:
            name = "/en/tournaments/" + "/".join(name.split(':')) + "/overview"
            tournament = parse_from_tournament_bio_fragment(name)
        return {
            'tournament': [{
                'name' if not url else 'url': name,
                'overview': tournament()
            }]
        }
