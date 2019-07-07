# Flask dependencies
from flask import Flask
from flask_restful import Resource, Api

# Endpoints
from Endpoints.RankingPageEndpoints import *
from Endpoints.RankingsHistoryEndpoint import *
from Endpoints.PlayerPageEndpoints import *

app = Flask(__name__)
api = Api(app)

api.add_resource(GetTopTen, '/api/top_10')
api.add_resource(RankingHistory, '/api/ranking_history/<string:name>')
api.add_resource(PlayerOverview, '/api/player_overview/<string:name>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
