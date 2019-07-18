# flask dependencies
from flask_restful import Resource
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser

# scraper dependencies
from scraper.Parser import parse_player_name
from scraper.PlayerTitlesPageParser import parse_player_titles_page


# Endpoints
class PlayerTitlesFinals(Resource):
    args = {'singles': fields.Bool(missing=True)}

    @use_kwargs(args)
    def get(self, name, singles):
        name = parse_player_name(name)
        return parse_player_titles_page(name, singles)
