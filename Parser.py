from Utils import get_site_content, logError, parse_with_soup, get_parsed_site_content
from Player import Player
import re

BASE = "https://www.atptour.com"
MAIN_URL = BASE + "/en/rankings"
SINGLES = "/singles"
DOUBLES = "/doubles"
PLAYERS_BASE_URL = "https://www.atptour.com"

space_regex = re.compile(r'( )+', re.IGNORECASE)


def entry_point(singles=True):
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


def get_top_10():
    """get_top_10"""
    html = entry_point()
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
    return "".join(space_regex.sub('-', name.strip()).lower().split())
    # return "".join(name.strip().replace(' ', '-').lower().split())


def get_player_bio(player_name, singles=True):
    """get_player_bio
    returns the url fragment for a player's ranking page

    :param player_name: name of the player
    :param singles: singles/doubles?
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


def parse_summary_table_row(row, player_details, career=True):
    if career:
        row_id = 'career_stats'
    else:
        row_id = 'current_year_stats'
    ranking_types = ['data-singles', 'data-doubles']
    tds = row.find_all('td')
    for td in tds:
        if td.has_attr('class'):
            if td['class'][0] == 'overview-year':
                player_details[row_id]['year'] = td.find(
                    'div').text.strip()
        if td.has_attr('colspan'):
            divs = td.find_all('div')
            for singles_attr in ranking_types:
                # for career-high ranking stats
                if int(td['colspan'].strip()) == 2:
                    # get career high ranking
                    rank_div = td.find('div', {'class': 'stat-value'})
                    if rank_div.has_attr(singles_attr):
                        player_details[row_id][
                            singles_attr]['rank'] = int(
                                rank_div[singles_attr].strip())
                    # get date of career high ranking
                    date_div = td.find('div', {'class': 'label-value'})
                    career_high_date_attr = singles_attr + "-label"
                    if date_div.has_attr(career_high_date_attr):
                        player_details[row_id][
                            singles_attr]['date_highest'] = str(date_div[career_high_date_attr].strip().split(' ')[-1])
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

                            player_details[row_id][
                                singles_attr][
                                    'rank_move'] = 0 if move is None else int(
                                        move + move_num)
                # filter for rank
                if any(div.text.strip() == 'Rank' for div in divs):
                    rank_div = td.find('div', {'class': 'stat-value'})
                    if rank_div.has_attr(singles_attr):
                        player_details[row_id][
                            singles_attr]['rank'] = int(
                                rank_div[singles_attr].strip())
                # filter for titles
                if any(div.text.strip() == 'Titles' for div in divs):
                    rank_div = td.find('div', {'class': 'stat-value'})
                    if rank_div.has_attr(singles_attr):
                        player_details[row_id][
                            singles_attr]['titles'] = int(
                                rank_div[singles_attr].strip())
                # filter for prize money
                if any(div.text.strip() in ('Prize Money', 'Prize Money Singles & Doubles combined') for div in divs):
                    rank_div = td.find('div', {'class': 'stat-value'})
                    if rank_div.has_attr(singles_attr):
                        player_details[row_id][
                            singles_attr]['prize_money'] = float(rank_div[singles_attr].strip()[1:].replace(",", ""))
                # filter for win-loss
                if any(div.text.strip() == "W-L" for div in divs):
                    wl_div = td.find('div', {'class': 'stat-value'})
                    if wl_div.has_attr(singles_attr):
                        player_details[row_id][
                            singles_attr]['w-l'] = [
                                int(x.strip()) for x in wl_div[
                                    singles_attr].strip().split('-')
                        ]


def build_player(player_content, player_name, player_bio):
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


def parse_player_page(player_name, singles=True):
    bio_fragment = get_player_bio(player_name, singles)
    if bio_fragment is None:
        logError("Player doesn't exist")
        return None
    else:
        PLAYER_FULL_URL = PLAYERS_BASE_URL + bio_fragment
    player_content = get_parsed_site_content(PLAYER_FULL_URL)
    return build_player(player_content, player_name, PLAYER_FULL_URL)


def get_player_rank(player_name, singles=True):
    bio_fragment = get_player_bio(player_name, singles)
    if bio_fragment is None:
        logError("Player doesn't exist")
    else:
        PLAYER_FULL_URL = PLAYERS_BASE_URL + bio_fragment
    return PLAYER_FULL_URL
