from typing import List
from .Utils import get_parsed_site_content, logError
from .Parser import get_player_bio, parse_player_name, player_link_cache
from .constants import *
from .Classes.TitleClasses import *
from .TournamentOverviewParser import parse_from_tournament_bio_fragment
from typing import Dict
from bs4 import Tag
from cachetools import cached
from .CacheUtils import player_titles_finals_cache


def parse_row(row: Tag, row_dict: Dict, titles: bool,
              tennis_type: bool = True):
    tds = row.select('td')
    for idx, td in enumerate(tds):
        # year
        if titles:
            if idx == 0:
                row_dict['year'] = int(td.text.strip())
        # number
        if idx == 1:
            row_dict['titles' if titles else 'finals']['number'] = int(
                td.text.strip())

        # tournaments
        if idx == 2:
            if tennis_type:
                tournies = td.select('a')
                for tourny in tournies:
                    row_dict['titles'
                             if titles else 'finals']['tournaments'].append({
                                 'tournament':
                                 tourny['data-ga-label'],
                                 'url':
                                 tourny['href']
                             })
            else:
                links = td.select('a')
                couple = 0
                for idx, link in enumerate(links):
                    if couple == 0:
                        tournament_with_partner = {
                            'tournament': {},
                            'doubles_partner': {}
                        }
                    # tournament
                    if idx % 2 == 0:
                        tournament_with_partner['tournament']['name'] = link[
                            'data-ga-label']
                        tournament_with_partner['tournament']['url'] = link[
                            'href']
                    # doubles partner
                    else:
                        tournament_with_partner['doubles_partner'][
                            'name'] = link['data-ga-label']
                        tournament_with_partner['doubles_partner'][
                            'url'] = link['href']

                    if couple == 1:
                        row_dict['titles' if titles else 'finals'][
                            'tournaments'].append(tournament_with_partner)
                        couple = 0
                    else:
                        couple += 1


def parse_table(tableTitles: Tag,
                tableFinals: Tag,
                tennis_type: str,
                year_range: List = None):
    type_dict = {'type': tennis_type, 'items': []}
    type_bool = True if tennis_type == 'singles' else False

    rows_title = tableTitles.select('tbody>tr')
    rows_final = tableFinals.select('tbody>tr')

    for row_title, row_final in zip(rows_title, rows_final):

        if year_range is not None:
            td = row_title.select_one('td')
            year = int(td.text.strip())
            if year not in year_range:
                continue

        year_row = {
            'year': 0,
            'titles': {
                'number': 0,
                'tournaments': [],
            },
            'finals': {
                'number': 0,
                'tournaments': []
            }
        }
        parse_row(row_title, year_row, True, type_bool)

        parse_row(row_final, year_row, False, type_bool)

        type_dict['items'].append(year_row)

    return type_dict


@cached(player_titles_finals_cache)
def parse_player_titles_page(parsed_name: str, singles=True, years: str = "*"):
    # parsed_name = parse_player_name(player_name)
    if years != "*":
        years_spl = years.strip().replace(' ', '').split(',')
        years = list(map(lambda x: int(x), years_spl))
    else:
        years = None

    bio = get_player_bio(parsed_name).replace('overview', '')
    url = PLAYER_TITLES_OVERVIEW_URL.format(bio)
    soup = get_parsed_site_content(url, default=False)

    Titles = soup.find('table',
                       {'id': 'singlesTitles' if singles else 'doublesTitles'})
    Finals = soup.find('table',
                       {'id': 'singlesFinals' if singles else 'doublesFinals'})

    res = parse_table(Titles, Finals, 'singles'
                      if singles else 'doubles', years)

    return {
        'singles' if singles else 'doubles': res,
    }
