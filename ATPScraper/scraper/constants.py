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
