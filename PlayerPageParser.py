from constants import *
from requests.exceptions import RequestException
from Utils import get_site_content, logError, parse_with_soup, get_parsed_site_content, get_api_call_content
from Parser import get_player_bio
from Classes.Player import Player
from typing import Dict, List
from functools import lru_cache
from bs4.element import Tag

"""
PLAYER OVERVIEW PAGE PARSER CONTENT BELOW
"""


def parse_summary_table_row(row: Tag,
                            player_details: Dict,
                            career: bool = True) -> None:
    """parse_summary_table_row

    :param row: row to parse in overview table on player's bio
    :type row: Tag
    :param player_details: Dict to modify
    :type player_details: Dict
    :param career: career or current year?
    :type career: bool
    :rtype: None
    """
    if career:
        row_id = 'career_stats'
    else:
        row_id = 'current_year_stats'
    ranking_types = ['data-singles', 'data-doubles']
    tds = row.find_all('td')
    for td in tds:
        if td.has_attr('class'):
            if td['class'][0] == 'overview-year':
                player_details[row_id]['year'] = td.find('div').text.strip()
        if td.has_attr('colspan'):
            divs = td.find_all('div')
            for singles_attr in ranking_types:
                # for career-high ranking stats
                if int(td['colspan'].strip()) == 2:
                    # get career high ranking
                    rank_div = td.find('div', {'class': 'stat-value'})
                    if rank_div.has_attr(singles_attr):
                        player_details[row_id][singles_attr]['rank'] = int(
                            rank_div[singles_attr].strip())
                    # get date of career high ranking
                    date_div = td.find('div', {'class': 'label-value'})
                    career_high_date_attr = singles_attr + "-label"
                    if date_div.has_attr(career_high_date_attr):
                        player_details[row_id][singles_attr][
                            'date_highest'] = str(date_div[
                                career_high_date_attr].strip().split(' ')[-1])
                # filter for ranking move
                if any(div.text.strip() == 'Move' for div in divs):
                    move_div = td.find('div', {'class': 'stat-value'})
                    if move_div.has_attr(singles_attr):
                        # move_Data = move_div['data-singles']
                        # move_num = move_Data.split('</span>')[-1].strip()
                        parsed_move_data = parse_with_soup(
                            move_div[singles_attr])
                        move_num = parsed_move_data.text.strip()
                        move_span = parsed_move_data.find('span')
                        if move_span.has_attr('class'):
                            if any(
                                    filter(
                                        lambda x: x.strip() == 'icon-double-up-arrow',
                                        move_span['class'])):
                                move = "+"
                            elif any(
                                    filter(
                                        lambda x: x.strip() == 'icon-double-down-arrow',
                                        move_span['class'])):
                                move = "-"
                            else:
                                move = None

                            player_details[row_id][singles_attr][
                                'rank_move'] = 0 if move is None else int(
                                    move + move_num)
                # filter for rank
                if any(div.text.strip() == 'Rank' for div in divs):
                    rank_div = td.find('div', {'class': 'stat-value'})
                    if rank_div.has_attr(singles_attr):
                        player_details[row_id][singles_attr]['rank'] = int(
                            rank_div[singles_attr].strip())
                # filter for titles
                if any(div.text.strip() == 'Titles' for div in divs):
                    rank_div = td.find('div', {'class': 'stat-value'})
                    if rank_div.has_attr(singles_attr):
                        player_details[row_id][singles_attr]['titles'] = int(
                            rank_div[singles_attr].strip())
                # filter for prize money
                if any(div.text.strip() in (
                        'Prize Money',
                        'Prize Money Singles & Doubles combined')
                       for div in divs):
                    rank_div = td.find('div', {'class': 'stat-value'})
                    if rank_div.has_attr(singles_attr):
                        pm_filtered = rank_div[singles_attr].strip()[
                            1:].replace(",", "")
                        if pm_filtered:
                            player_details[row_id][
                                singles_attr]['prize_money'] = float(
                                    rank_div[singles_attr].strip()[1:].replace(
                                        ",", ""))
                        else:
                            player_details[row_id][singles_attr][
                                'prize_money'] = 0
                # filter for win-loss
                if any(div.text.strip() == "W-L" for div in divs):
                    wl_div = td.find('div', {'class': 'stat-value'})
                    if wl_div.has_attr(singles_attr):
                        player_details[row_id][singles_attr]['w-l'] = [
                            int(x.strip())
                            for x in wl_div[singles_attr].strip().split('-')
                        ]


@lru_cache()
def build_player(player_content, player_name, player_bio) -> Player:
    """build_player
    https://docs.python.org/3/library/functools.html#functools.lru_cache
    :param player_content: BeautifulSoup parsed player page content
    :param player_name: name of the player
    :param player_bio: player's bio link
    :rtype: Player
    """
    player_details = {
        'name': player_name,
        'bio_url': player_bio,
        'current_year_stats': {
            'data-singles': {},
            'data-doubles': {}
        },
        'career_stats': {
            'data-singles': {},
            'data-doubles': {}
        },
    }
    data_table = player_content.select('.players-stats-table>tbody>tr')
    for row in data_table:
        if row.find("th") is not None:
            parse_summary_table_row(row, player_details, False)
        else:
            parse_summary_table_row(row, player_details, True)

    return Player(**player_details)


def parse_player_page(player_name: str, singles: bool = True) -> Dict:
    """parse_player_page

    :param player_name: name of the player
    :type player_name: str
    :param singles: singles or doubles?
    :type singles: bool
    :rtype: Dict
    """
    bio_fragment = get_player_bio(player_name, singles)
    if bio_fragment is None:
        logError("Player doesn't exist")
        return None
    else:
        PLAYER_FULL_URL = PLAYERS_BASE_URL + bio_fragment
    player_content = get_parsed_site_content(PLAYER_FULL_URL)
    return build_player(player_content, player_name, PLAYER_FULL_URL)


def get_player_rank(player_name: str, singles: bool = True) -> int:
    """get_player_rank

    :param player_name: name of the player
    :type player_name: str
    :param singles: singles or doubles?
    :type singles: bool
    :rtype: int
    """
    try:
        bio_fragment = get_player_bio(player_name, singles)
    except ValueError as e:
        logError(e)
        return -1
    if bio_fragment is None:
        logError("Player doesn't exist")
        return -1
    else:
        PLAYER_FULL_URL = PLAYERS_BASE_URL + bio_fragment
    player_content = get_parsed_site_content(PLAYER_FULL_URL)
    player = build_player(player_content, player_name, PLAYER_FULL_URL)
    return player.cy_stats['data-singles'][
        'rank'] if singles else player.cy_stats['data-doubles']['rank']

# print(get_player_rank('john isner'))
