from time import time, localtime
# from .constants import start_date
from typing import List
from .Classes.Ranking import Ranking
from .constants import PLAYERS_RANKING_HISTORY, BASE
from .Utils import get_parsed_site_content, logError
from .Parser import get_player_bio, parse_player_name
from .PlayerPageParser import player_bio_cache
from functools import lru_cache
from cachetools import cached
from .CacheUtils import clear_caches, check_timer, ranking_history_cache


# @lru_cache()
@cached(ranking_history_cache)
def get_player_ranking_history(player_name: str) -> List[Ranking]:
    """get_player_ranking_history

    :param player_name: name of the player
    :type player_name: str
    :rtype: List[Ranking]
    """
    # curr_time = localtime(time())
    # curr_mon, curr_day = curr_time.tm_mon, curr_time.tm_mday
    # if not start_date[0] - curr_mon or not start_date[1] - curr_day:
    #     ranking_history_cache.clear()
    check_timer()
    parsed_name = parse_player_name(player_name)
    player = None
    if parsed_name in list(map(lambda x: x[0], player_bio_cache.__iter__())):
        player = player_bio_cache[(parsed_name, )]
        old_rank_hist = player.ranking_history
        if old_rank_hist is not None:
            return old_rank_hist
    try:
        player_bio = get_player_bio(player_name)
    except ValueError as e:
        logError(e)
        # since you're cacheing, you have to figure out how to handle this case if it returns the error response
        return []
    # get_player_bio returns the overview url -> need to replace this
    url = BASE + player_bio.replace('/overview', '') + PLAYERS_RANKING_HISTORY
    soup = get_parsed_site_content(url)
    ranking_history = []
    for ranking in soup.select(
            '#playerRankHistoryContainer > table > tbody > tr'):
        tds = ranking.find_all('td')
        ranking = {}
        for i in range(len(tds)):
            text = tds[i].text.strip()
            if i == 0:
                ranking['date'] = text
            elif i == 1:
                ranking['singles'] = text
            elif i == 2:
                ranking['doubles'] = text
        ranking_history.append(Ranking(**ranking))

    # update the cache
    if player is not None:
        player_bio_cache.__setitem__((parsed_name, ), ranking_history)
    return ranking_history
