import re
from datetime import datetime
BASE = "https://www.atptour.com"
MAIN_URL = BASE + "/en/rankings"
SINGLES = "/singles"
DOUBLES = "/doubles"
PLAYERS_BASE_URL = "https://www.atptour.com"
PLAYER_SEARCH_URL = "/en/-/ajax/playersearch/PlayerUrlSearch?searchTerm="
PLAYERS_RANKING_HISTORY = "/rankings-history"
PLAYERS_WIN_LOSS_STATS = "/fedex-atp-win-loss"
start_date = datetime(2019, 7, 7, 23, 8, 45, 474911)
space_regex = re.compile(r'( )+', re.IGNORECASE)
capital_regex = re.compile(r'(?=[A-Z])')

