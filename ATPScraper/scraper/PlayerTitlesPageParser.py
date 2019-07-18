from .Utils import get_parsed_site_content, logError 
from .Parser import get_player_bio, parse_player_name, player_link_cache
from .constants import *
from .Classes.TitleClasses import *
from .TournamentOverviewParser import parse_from_tournament_bio_fragment
from typing import Dict
from bs4 import Tag
from cachetools import cached
from .CacheUtils import player_titles_finals_cache


def parse_row(row: Tag, row_dict: Dict, titles: bool):
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
            tournies = td.select('a')
            for tourny in tournies:
                row_dict['titles' if titles else 'finals'][
                    'tournaments'].append(
                        parse_from_tournament_bio_fragment(
                            tourny['href'].strip())())


def parse_table(tableTitles: Tag, tableFinals: Tag, tennis_type: Dict):
    type_dict = {'type': tennis_type, 'items': []}

    rows_title = tableTitles.select('tbody>tr')
    rows_final = tableFinals.select('tbody>tr')

    for row_title, row_final in zip(rows_title, rows_final):
        year_row = {
            'year': 0,
            'titles': {
                'number': 0,
                'tournaments': []
            },
            'finals': {
                'number': 0,
                'tournaments': []
            }
        }
        parse_row(row_title, year_row, True)

        parse_row(row_final, year_row, False)


        type_dict['items'].append(year_row)

    return type_dict



@cached(player_titles_finals_cache)
def parse_player_titles_page(parsed_name: str, singles=True):
    # parsed_name = parse_player_name(player_name)
    bio = get_player_bio(parsed_name).replace('overview', '')
    url = PLAYER_TITLES_OVERVIEW_URL.format(bio)
    soup = get_parsed_site_content(url,default=False)

    Titles = soup.find('table', {'id': 'singlesTitles' if singles else 'doublesTitles'})
    Finals = soup.find('table', {'id': 'singlesFinals' if singles else 'doublesFinals'})

    res = parse_table(Titles, Finals, 'singles' if singles else 'doubles')

    return {
        'singles' if singles else 'doubles': res ,
    }

