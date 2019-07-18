# flask dependencies
from flask_restful import Resource
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser

# scraper dependencies
from scraper.PlayerWinLossPageParser import get_player_win_loss_stats, get_tour_stats
from scraper.Parser import parse_player_name


# Endpoints
class PlayerWinLoss(Resource):
    """PlayerWinLoss"""
    args = {'tour': fields.Str(missing='*')}

    @use_kwargs(args)
    def get(self, name, tour):
        """get

        api/player_win_loss/{name}?tour={tour}

        :param name: name of the player to parse
        :param tour: tour type {Default: *}
        """
        name = parse_player_name(name)
        return get_tour_stats(name, tour)()
