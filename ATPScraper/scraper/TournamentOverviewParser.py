from .Utils import get_parsed_site_content, logError, get_api_call_content
from .Parser import parse_player_name  # used to parse tournament name also
from .constants import *
from .Classes.TitleClasses import *
from cachetools import cached
from .CacheUtils import tournament_overview_cache


def parse_from_tournament_bio_fragment(bio_frag=str):
    tournament_dict = {
        'name': '',
        'surface': '',
        'bio': '',
        'level': '',
        'draw_size': [],
        'prize_money': '',
        'total_financial_commitment': ''
    }

    TOURNAMENT_URL = BASE + bio_frag
    parsed_tournament_name = bio_frag.split('/')[3].strip()
    t_id = bio_frag.split('/')[4].strip()
    tournament_dict['bio'] = TOURNAMENT_URL
    tournament_dict['name'] = parsed_tournament_name

    in_cache = True
    if tournament_overview_cache.__contains__(parsed_tournament_name):
        return tournament_overview_cache[parsed_tournament_name]
    else:
        in_cache = False

    # there is an issue with non-official atp tournaments such as ATP cup and davis cup
    # there also seems to be issues with tournies that change location
    # ie. MTL/TOR
    soup = get_parsed_site_content(TOURNAMENT_URL)
    if not soup:
        tmp = parsed_tournament_name + "/" + t_id
        if tmp in tournament_names_alts:
            TOURNAMENT_URL = TOURNAMENT_URL.replace(tmp,
                                                    tournament_names_alts[tmp])
            soup = get_parsed_site_content(TOURNAMENT_URL)
        if not soup:
            TOURNAMENT_SEARCH_URL_FULL = BASE + TOURNAMENT_SEARCH_URL.format(
                parsed_tournament_name)
            # there is an issue with non-official atp tournaments such as ATP cup and davis cup
            content = get_api_call_content(TOURNAMENT_SEARCH_URL_FULL)
            if not content['items']:
                return Tournament(**tournament_dict)
            TOURNAMENT_URL = BASE + content['items'][0]['Url']
            soup = get_parsed_site_content(TOURNAMENT_URL)

            if not soup:
                return Tournament(**tournament_dict)

    logo = soup.find('div', {'class': 'tournmanet-logo'})
    img = logo.find('img')
    alt = img['alt'].strip()

    if alt:
        alt_num = alt.split(' ')[-1]
        tournament_dict['level'] = alt_num

    # parent table
    tournament_hero_grid = soup.find('div', {'class': 'tournament-hero-grid'})

    # singles and doubles draw sizes
    bracket_bottom = tournament_hero_grid.find('div',
                                               {'class': 'bracket-bottom'})
    singles_bracket = bracket_bottom.find('div', {'class': 'bracket-sgl'})
    singles_bracket_num = singles_bracket.find('div', {
        'class': 'item-inline-value'
    }).text.strip()
    doubles_bracket = bracket_bottom.find('div', {'class': 'bracket-dbl'})
    doubles_bracket_num = doubles_bracket.find('div', {
        'class': 'item-inline-value'
    }).text.strip()
    tournament_dict['draw_size'] = [
        int(singles_bracket_num),
        int(doubles_bracket_num)
    ]

    # surface (if there is one)
    surface_bottom = tournament_hero_grid.find('div',
                                               {'class': 'surface-bottom'})
    surface = surface_bottom.find('div', {'class': 'item-value'}).text
    tournament_dict['surface'] = surface

    # prize-money given out
    prize_money_bottom = tournament_hero_grid.find(
        'div', {'class': 'prize-money-bottom'})
    pm = prize_money_bottom.find('div', {'class': 'item-value'}).text.strip()
    tournament_dict['prize_money'] = pm

    # total financial commitment
    tfc_bottom = tournament_hero_grid.find('div', {'class': 'tfc-bottom'})
    tfc = tfc_bottom.find('div', {'class': 'item-value'}).text.strip()
    tournament_dict['total_financial_commitment'] = tfc

    res = Tournament(**tournament_dict)

    if not in_cache:
        tournament_overview_cache.__setitem__(parsed_tournament_name, res)

    return res


@cached(tournament_overview_cache)
def ParseTournametOverViewPage(parsed_tournament_name: str):
    TOURNAMENT_SEARCH_URL_FULL = BASE + TOURNAMENT_SEARCH_URL.format(
        parsed_tournament_name)
    # there is an issue with non-official atp tournaments such as ATP cup and davis cup
    content = get_api_call_content(TOURNAMENT_SEARCH_URL_FULL)
    if not content['items']:
        return Tournament()
    TOURNAMENT_URL = BASE + content['items'][0]['Url']
    soup = get_parsed_site_content(TOURNAMENT_URL)
    logo = soup.find('div', {'class': 'tournmanet-logo'})
    img = logo.find('img')
    alt = img['alt'].strip()
    tournament_dict = {
        'name': '',
        'surface': '',
        'bio': '',
        'level': '',
        'draw_size': [],
        'prize_money': '',
        'total_financial_commitment': ''
    }

    tournament_dict['bio'] = TOURNAMENT_URL
    tournament_dict['name'] = parsed_tournament_name
    if alt:
        alt_num = alt.split(' ')[-1]
        tournament_dict['level'] = alt_num
    else:
        tournament_dict['level'] = 'grand_slam'

    # parent table
    tournament_hero_grid = soup.find('div', {'class': 'tournament-hero-grid'})

    # singles and doubles draw sizes
    bracket_bottom = tournament_hero_grid.find('div',
                                               {'class': 'bracket-bottom'})
    singles_bracket = bracket_bottom.find('div', {'class': 'bracket-sgl'})
    singles_bracket_num = singles_bracket.find('div', {
        'class': 'item-inline-value'
    }).text.strip()
    doubles_bracket = bracket_bottom.find('div', {'class': 'bracket-dbl'})
    doubles_bracket_num = doubles_bracket.find('div', {
        'class': 'item-inline-value'
    }).text.strip()
    tournament_dict['draw_size'] = [
        int(singles_bracket_num),
        int(doubles_bracket_num)
    ]

    # surface (if there is one)
    surface_bottom = tournament_hero_grid.find('div',
                                               {'class': 'surface-bottom'})
    surface = surface_bottom.find('div', {'class': 'item-value'}).text
    tournament_dict['surface'] = surface

    # prize-money given out
    prize_money_bottom = tournament_hero_grid.find(
        'div', {'class': 'prize-money-bottom'})
    pm = prize_money_bottom.find('div', {'class': 'item-value'}).text.strip()
    tournament_dict['prize_money'] = pm

    # total financial commitment
    tfc_bottom = tournament_hero_grid.find('div', {'class': 'tfc-bottom'})
    tfc = tfc_bottom.find('div', {'class': 'item-value'}).text.strip()
    tournament_dict['total_financial_commitment'] = tfc

    return Tournament(**tournament_dict)
