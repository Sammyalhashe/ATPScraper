# Flask dependencies
from flask import Flask
from flask_restful import Resource, Api

# Endpoints
from Endpoints.RankingPageEndpoints import *
from Endpoints.RankingsHistoryEndpoint import *
from Endpoints.PlayerPageEndpoints import *
from Endpoints.PlayerWinLossPageEndpoints import *
from Endpoints.TournamentOverviewEndpoints import *
from Endpoints.PlayerTitlesEndpoints import *

# api init
app = Flask(__name__)
api = Api(app)

# api resources
api.add_resource(GetTopTen, '/api/top_10')
api.add_resource(RankingHistory, '/api/ranking_history/<string:name>')
api.add_resource(PlayerOverview, '/api/player_overview/<string:name>')
api.add_resource(PlayerRanking, '/api/player_ranking/<string:name>')
api.add_resource(PlayerWinLoss, '/api/player_win_loss/<string:name>')
api.add_resource(TournamentOverview, '/api/tournament_overview/<string:name>')
api.add_resource(PlayerTitlesFinals, '/api/<string:name>/titles')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
