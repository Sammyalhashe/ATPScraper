from typing import List
from Classes.Ranking import Ranking
from constants import PLAYERS_RANKING_HISTORY, BASE
from Utils import get_parsed_site_content
from Parser import get_player_bio, logError
from functools import lru_cache


@lru_cache()
def get_player_ranking_history(player_name: str) -> List[Ranking]:
    """get_player_ranking_history

    :param player_name: name of the player
    :type player_name: str
    :rtype: List[Ranking]
    """
    try:
        player_bio = get_player_bio(player_name)
    except ValueError as e:
        logError(e)
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
    return ranking_history
