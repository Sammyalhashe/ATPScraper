# other dependencies
import os

# Flask dependencies
from flask import Flask, render_template
from flask_restful import Resource, Api

# Endpoints
from Endpoints.RankingPageEndpoints import *
from Endpoints.RankingsHistoryEndpoint import *
from Endpoints.PlayerPageEndpoints import *
from Endpoints.PlayerWinLossPageEndpoints import *
from Endpoints.TournamentOverviewEndpoints import *
from Endpoints.PlayerTitlesEndpoints import *
from Endpoints.PlayerRankingBreakdownEndpoints import *

# api init
if os.environ.get('DEV', 'development') == 'production':
    app = Flask(
        __name__, static_folder='build/static', template_folder='build')
else:
    app = Flask(__name__)
api = Api(app)


# main page
@app.route("/")
def hello():
    if os.environ.get('DEV', 'development') == 'production':
        return render_template('index.html')
    else:
        return 'dev-home'


# api resources
api.add_resource(GetTopTen, '/api/top_10')
api.add_resource(RankingHistory, '/api/ranking_history/<string:name>')
api.add_resource(PlayerOverview, '/api/player_overview/<string:name>')
api.add_resource(PlayerRanking, '/api/player_ranking/<string:name>')
api.add_resource(PlayerWinLoss, '/api/player_win_loss/<string:name>')
api.add_resource(TournamentOverview, '/api/tournament_overview/<string:name>')
api.add_resource(PlayerTitlesFinals, '/api/<string:name>/titles')
api.add_resource(PlayerRankingsBreakdown, '/api/<string:name>/rankings_breakdown')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(port)
    app.run(host="0.0.0.0", port=port, debug=False)
