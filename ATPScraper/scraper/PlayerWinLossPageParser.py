from .Utils import get_parsed_site_content, logError
from .Parser import get_player_bio, logError, parse_player_name, player_link_cache
from .constants import *
from .Classes.PlayerWinLoss import PlayerWinLossRecords, PlayerWinLossRecord
from .Classes.WinLossStat import MatchRecord, PressurePoints, Environment, Other, WinLossStat
from .CacheUtils import player_win_loss_cache
from cachetools import cached
from bs4 import Tag
from typing import Dict


def parse_win_loss_stat_row(row: Tag, win_loss_stat: Dict = {}) -> WinLossStat:
    """parse_win_loss_stat_row

    :param row: row to parse in mega-table
    :type row: Tag
    :param win_loss_stat: dict to fill up
    :type win_loss_stat: Dict
    :rtype: WinLossStat
    """
    # parse the inner tables
    innerWinLossCells = row.select('td>.inner-win-loss-cells')
    encounter_num = 0
    for innerWinLossCell in innerWinLossCells:
        innerWinLossCellsTds = innerWinLossCell.select('tbody>tr>td')
        WinLoss = []
        for iWLCT in innerWinLossCellsTds:
            if iWLCT.text.strip().isdigit():
                WinLoss.append(int(iWLCT.text.strip()))
        if encounter_num == 0:
            win_loss_stat['ytd_wl'] = WinLoss
        elif encounter_num == 1:
            win_loss_stat['car_wl'] = WinLoss
        encounter_num += 1

    # parse everything else
    inner_tds = row.select('td')
    encounter_num = 0
    for inner_td in inner_tds:
        if not inner_td.parent.parent.parent['class'][
                0] == 'inner-win-loss-cells':
            if encounter_num < 2:
                try:
                    floated = float(inner_td.text.strip())
                    if encounter_num == 0:
                        win_loss_stat['ytd_fedex'] = floated
                    elif encounter_num == 1:
                        win_loss_stat['car_fedex'] = floated
                    encounter_num += 1
                except ValueError:
                    continue
            else:
                try:
                    inted = int(inner_td.text.strip())
                    if encounter_num == 2:
                        win_loss_stat['titles'] = inted
                except ValueError:
                    continue
    win_loss_stat = WinLossStat(**win_loss_stat)
    return win_loss_stat


def parse_category_label(label: str) -> str:
    """parse_category_label

    removes *'s and round brackets and periods and transforms to lowercase

    :param label: label to parse
    :type label: str
    :rtype: str
    """
    return number_first_regex.sub(
        '_',
        space_regex.sub(
            '_',
            label.strip().lower().replace('*', '').replace('(', '').replace(
                ')', '').replace('.', '')))


def get_player_win_loss_stats_for_tour(player_name: str,
                                       tour_type: str = 'tour'
                                       ) -> PlayerWinLossRecord:
    """get_player_win_loss_stats_for_tour

    Returns a PlayerWinLossRecord for a specific tour

    :param player_name: unparsed player name
    :type player_name: str
    :param tour_type:
    :type tour_type: str
    :rtype: PlayerWinLossRecord
    """
    parsed_name = parse_player_name(player_name)
    stats_for_tour = None
    player_bio = get_player_bio(parsed_name)
    print(player_bio)
    player_id = player_bio.split('/')[-2]
    # try:
    #     if player_link_cache.__contains__(parsed_name):
    #         print(list(map(lambda x: x[0], player_link_cache.__iter__())))
    #         player_bio = player_link_cache[parsed_name]
    #     else:
    #         player_bio = get_player_bio(parsed_name)
    #     player_id = player_bio.split('/')[-2]
    # except ValueError as e:
    #     logError(e)
    #     # return empty records object
    #     return PlayerWinLossRecord()
    url = PLAYER_WIN_LOSS_URLS.format(tour_type, player_id)
    soup = get_parsed_site_content(url)
    classes = [MatchRecord, PressurePoints, Environment, Other]
    # start parsing
    megaTables = soup.select('.mega-table')
    player_win_loss_record = {}
    for megaTable in megaTables:
        thead_rows = megaTable.select('thead>th')
        tbody_rows = megaTable.select('tbody>tr')
        # if we are dealing with the Match Record sub table
        first_thead = megaTable.select_one('thead>th')
        if first_thead.parent.parent['class'][0] == 'mega-table':
            # if any(th.text.strip() == 'Match Record' for th in thead_rows):
            wl_stat_collection = {}
            for row in tbody_rows:
                tds = row.select('td')
                tdone = row.select_one('td')
                if not tdone.parent.parent.parent['class'][
                        0] == 'inner-win-loss-cells':
                    parsed_cat = parse_category_label(tdone.text)
                    wl_stat = parse_win_loss_stat_row(row)
                    wl_stat_collection[parsed_cat] = wl_stat

            # decide which class we are dealing with
            for class_type in classes:
                if space_regex.sub(
                        '', first_thead.text.strip()) == class_type.__name__:
                    name = class_type.__name__
                    player_win_loss_record[name] = class_type(
                        **wl_stat_collection)
                    break
    win_loss_object = PlayerWinLossRecord(**player_win_loss_record)
    return win_loss_object


@cached(player_win_loss_cache)
def get_player_win_loss_stats(player_name: str) -> PlayerWinLossRecords:
    """get_player_win_loss_stats

    builds a complete PlayerWinLossRecords object

    :param player_name: unparsed player name
    :type player_name: str
    :rtype: PlayerWinLossRecords
    """
    parsed_name = parse_player_name(player_name)
    player_bio = get_player_bio(parsed_name)
    # try:
    #     if player_link_cache.__contains__(parsed_name):
    #         print(list(map(lambda x: x[0], player_link_cache.__iter__())))
    #         player_bio = player_link_cache[parsed_name]
    #     else:
    #         player_bio = get_player_bio(parsed_name)
    # except ValueError as e:
    #     logError(e)
    #     # return empty records object
    #     return PlayerWinLossRecords()
    player_win_loss_records = {}
    win_loss_types = ["tour", "challenger", "itf"]
    for win_loss_type in win_loss_types:
        player_win_loss_records[
            win_loss_type] = get_player_win_loss_stats_for_tour(
                parsed_name, tour_type=win_loss_type)
    return PlayerWinLossRecords(**player_win_loss_records)


def get_tour_stats(player_name: str, tour_type: str = '*'):
    """get_tour_stats

    Entry point for the api.
    tour_type is a url parameter query that defaults to "*" which means "all"

    If a specific tour_type is mentioned, it does not build the entire
    PlayerWinLossRecords object, and only returns a PlayerWinLossRecord object

    :param player_name: unparsed player name
    :type player_name: str
    :param tour_type:
    :type tour_type: str
    """
    # build complete PlayerWinLossRecords object
    if tour_type == "*":
        return get_player_win_loss_stats(player_name)

    parsed_name = parse_player_name(player_name)

    # if the player_win_loss_cache contains an entry corresponding to
    # parsed_name, pull it out. If is has a tour_type entry, return that
    # instead of parsing. Otherwise parse and set its tour_type value to the
    # result for future usage
    if player_win_loss_cache.__contains__(parsed_name):
        if player_win_loss_cache[parsed_name][tour_type] is not None:
            return player_win_loss_cache[parsed_name][tour_type]
        tour_record = get_player_win_loss_stats_for_tour(
            player_name, tour_type)
        if tour_type == 'tour':
            player_win_loss_cache[parsed_name].set_atp(tour_record)
        if tour_type == 'challenger':
            player_win_loss_cache[parsed_name].set_challenger(tour_record)
        if tour_type == 'itf':
            player_win_loss_cache[parsed_name].set_itf(tour_record)

        return tour_record
    # if there is no entry in the cache, just go ahead and parse and return
    # the result
    else:
        tour_record = get_player_win_loss_stats_for_tour(
            player_name, tour_type)
        return tour_record
