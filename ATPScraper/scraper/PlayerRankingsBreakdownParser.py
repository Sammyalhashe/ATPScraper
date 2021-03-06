from typing import List
from .Utils import get_parsed_site_content, logError
from .Parser import get_player_bio, parse_player_name
from .constants import PLAYER_RANKINGS_BREAKDOWN_URL
from .CacheUtils import parse_player_ranking_breakdown_cache
from cachetools import cached
from bs4 import Tag


def parse_megatable_row(row: Tag):
    ret_object = {}
    tds = row.select('td')
    for idx, td in enumerate(tds):
        if idx == 0:
            ret_object['date'] = td.text.strip()
        if idx == 1:
            ret_object['tournament'] = {}
            ret_object['tournament']['name'] = td.text.strip()
            ret_object['tournament']['bio'] = td.find('a')['href']
        if idx == 2:
            ret_object['result'] = td.text.strip()

        if idx == 3:
            ret_object['points'] = int(td.text.strip().replace(',',
                                                               '').replace(
                                                                   '.', ''))

        if idx == 4:
            ret_object['close-date'] = td.text.strip()

    return ret_object


def parse_megatable(megaTable: Tag, table_name):
    ret_object = {'name': table_name}
    parsed_rows = []
    tbody = megaTable.find('tbody')
    rows = tbody.select('tr')
    for row in rows:
        parsed_rows.append(parse_megatable_row(row))
    ret_object['items'] = parsed_rows
    return ret_object


@cached(parse_player_ranking_breakdown_cache)
def parse_player_ranking_breakdown(parsed_name: str):
    name = parse_player_name(parsed_name)
    bio = get_player_bio(name).replace('overview', '')
    url = PLAYER_RANKINGS_BREAKDOWN_URL.format(bio)
    soup = get_parsed_site_content(url)
    container = soup.find('div', {'id': 'playerRankBreakdownContainer'})
    megaTables = container.select('.mega-table')

    tournament_types = []
    # we can ignore the table in the zeroeth index as
    # it mainly relates to current ranking values
    # that can be recieved from another endpoint
    # first table is ATP
    tournament_types.append(
        parse_megatable(megaTables[1], 'world-championship'))
    tournament_types.append(parse_megatable(megaTables[2], 'grand-slams'))
    tournament_types.append(parse_megatable(megaTables[3], 'atp-masters-1000'))
    tournament_types.append(parse_megatable(megaTables[4], 'atp-tour-500'))

    return {'items': tournament_types}
