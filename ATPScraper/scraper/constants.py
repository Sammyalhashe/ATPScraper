import re
from datetime import datetime
BASE = "https://www.atptour.com"
MAIN_URL = BASE + "/en/rankings"
SINGLES = "/singles"
DOUBLES = "/doubles"
PLAYERS_BASE_URL = "https://www.atptour.com"
PLAYER_SEARCH_URL = "/en/-/ajax/playersearch/PlayerUrlSearch?searchTerm="
TOURNAMENT_SEARCH_URL = "/en/-/ajax/PredictiveContentSearch/GetTournamentResults/{0}"
PLAYERS_RANKING_HISTORY = "/rankings-history"
PLAYERS_WIN_LOSS_STATS = "/fedex-atp-win-loss"
PLAYER_WIN_LOSS_URLS = BASE + "/en/content/ajax/player-match-record-page?matchRecordType={0}&playerId={1}"
PLAYER_TITLES_OVERVIEW_URL = BASE + "{}" + "titles-and-finals"
PLAYER_RANKINGS_BREAKDOWN_URL = BASE + "{}" + "rankings-breakdown"
start_date = datetime(2019, 7, 7, 23, 8, 45, 474911)
space_regex = re.compile(r'( )+', re.IGNORECASE)
capital_regex = re.compile(r'(?=[A-Z])')
number_first_regex = re.compile(r'^(?=[0-9])')

# contradictory tournament names
tournament_names_alts = {
    'atp-finals/605': 'nitto-atp-finals/605',
    'tennis-masters-cup/605': 'nitto-atp-finals/605',
    'toronto/421': 'montreal/421'
}

headers = {
    "Host": "www.atptour.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:83.0) Gecko/20100101 Firefox/83.0",
    "Accept": "image/webp,*/*",
    "Accept-Language": "en-CA,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.atptour.com/en/-/ajax/playersearch/PlayerUrlSearch?searchTerm=rogerfederer",
    "Cookie": "__cfduid=d0cc39a9db4608c3f1a2406b53d3e6e921606058338; atpModalContainer=%2Fen%2Fplayers%2Froger-federer%2Ff324%2Foverview; __cf_bm=9b85edff842e0f0913b2d30e07196b65714a9734-1606063387-1800-ASqCuRAh05On6EplJjj6903WoCadH0BQ0JHccKj3Tab/WkM4YfjO8I5+/sfXRU3qq2iqDIUkdcUmJb/lbZ8u6fE="
}
