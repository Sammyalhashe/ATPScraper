from time import time, localtime
from .constants import *
from requests.exceptions import RequestException
from .Utils import logError, get_parsed_site_content, get_api_call_content
from typing import Dict, List
from functools import lru_cache
from bs4.element import Tag
from cachetools import cached
from .CacheUtils import clear_caches, check_timer, player_link_cache
"""
HOME RANKING CONTENT BELOW
"""


def entry_point(singles: bool = True):
    """entry_point
    Entry page for the rankings

    :param singles: If we are looking at Singles (True) or Doubles (False)
    """
    if singles:
        EXTRA = SINGLES
    else:
        EXTRA = DOUBLES
    raw = get_parsed_site_content(MAIN_URL + EXTRA)
    if raw is not None:
        return raw
    else:
        logError("Something went wrong")
        return None


def get_top_10() -> List[str]:
    """get_top_10"""
    html = entry_point()
    if html is None:
        return []
    p = 0
    players = []
    for player in html.select('.player-cell>a'):
        players.append(player.text)
        if p == 9:
            break
        p += 1
    return players


def parse_player_name(name):
    """parse_player_name
    Parses a player's name to be consistent. It removes all inner white-space
    and replaces in with "-" as well as making the string lowercase as the
    url is lowercase.

    :param name: name to be parsed
    """
    name = name.strip()
    # split by capital letters
    name = capital_regex.sub(' ', name).strip()
    # split by spaces
    return "".join(space_regex.sub('-', name).lower().split())


def parse_player_search_response(res: Dict) -> Dict:
    """parse_player_search_response

    :param res: json.loaded response from player search
    :type res: Dict
    :rtype: Dict
    """
    if not res['items']:
        raise ValueError("Player does not exist")
    parsed_response = {}
    parsed_response['Key'] = res['items'][0]['Key']
    parsed_response['Value'] = res['items'][0]['Value']
    return parsed_response


def search_for_player(player_name: str) -> str:
    """search_for_player

    :param player_name: player name to search
    :type player_name: str
    :rtype: str
    """
    try:
        content = get_api_call_content(BASE + PLAYER_SEARCH_URL + player_name)
    except RequestException as e:
        logError(e)
        return None
    if not content:
        logError("Player does not exist")
        return None
    try:
        return parse_player_search_response(content)
    except ValueError as e:
        logError(e)
        return None


# @lru_cache()
@cached(player_link_cache)
def get_player_bio(player_name: str, singles: bool = True) -> str:
    """get_player_bio
    returns the url fragment for a player's ranking page

    :param player_name: name of the player
    :param singles: singles/doubles?
    """
    # curr_time = localtime(time())
    # curr_mon, curr_day = curr_time.tm_mon, curr_time.tm_mday
    # if not start_date[0] - curr_mon or not start_date[1] - curr_day:
    #     player_link_cache.clear()
    check_timer()
    dict_with_bio_frag = search_for_player(player_name)
    if not dict_with_bio_frag:
        # raise ValueError("Player does not exist")
        return ""

    return dict_with_bio_frag['Value']
    """
    player_name = parse_player_name(player_name)
    html = entry_point()
    if html is None:
        logError("Player does not exist")
        return None
    for player in html.select('.player-cell>a'):
        text = parse_player_name(player.text)
        if player_name == text:
            return player['href']
    return None
    """
