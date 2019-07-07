import re
BASE = "https://www.atptour.com"
MAIN_URL = BASE + "/en/rankings"
SINGLES = "/singles"
DOUBLES = "/doubles"
PLAYERS_BASE_URL = "https://www.atptour.com"
PLAYER_SEARCH_URL = "/en/-/ajax/playersearch/PlayerUrlSearch?searchTerm="
PLAYERS_RANKING_HISTORY = "/rankings-history"

space_regex = re.compile(r'( )+', re.IGNORECASE)


