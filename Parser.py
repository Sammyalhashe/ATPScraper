from Utils import get_site_content, logError
from bs4 import BeautifulSoup as bs

BASE = "https://www.atptour.com"
MAIN_URL = BASE + "/en/rankings"
SINGLES = "/singles"
DOUBLES = "/doubles"
PLAYERS_BASE_URL = "https://www.atptour.com/"

def entry_point(singles=True):
    if singles:
        EXTRA = SINGLES
    else:
        EXTRA = DOUBLES
    raw = get_site_content(MAIN_URL+EXTRA)
    if raw is not None:
        return raw
    else:
        logError("Something went wrong")
        return None


def parse_with_soup(resp):
    if resp is not None:
        parsed = bs(resp, 'html.parser')
        return parsed
    else:
        logError("Response is not valid")
        return None

def get_top_10():
    entry = entry_point()
    html = parse_with_soup(entry)
    p = 0
    for player in html.select('.player-cell>a'):
        print(player.text)
        if p == 9:
            break
        p += 1

def parse_player_name(name):
    return "".join(name.strip().replace(' ', '-').lower().split())

def get_player_info(player_name, singles=True):
    player_name = parse_player_name(player_name)
    entry = entry_point()
    html = parse_with_soup(entry)
    for player in html.select('.player-cell>a'):
        text = parse_player_name(player.text)
        if player_name == text:
            return player['href']


print(get_player_info('Taylor fritz'))
