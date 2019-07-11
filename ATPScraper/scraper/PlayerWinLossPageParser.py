from .Utils import get_parsed_site_content, logError
from .Parser import get_player_bio, logError, parse_player_name
from .constants import *
from .Classes.PlayerWinLoss import PlayerWinLossRecords, PlayerWinLossRecord
from .Classes.WinLossStat import MatchRecord, PressurePoints, Environment, Other, WinLossStat


def get_player_win_loss_stats(player_name: str) -> PlayerWinLossRecords:
    
    parsed_name = parse_player_name(player_name)
    try:
        player_bio = get_player_bio(parsed_name)
    except ValueError as e:
        logError(e)
        # return empty records object
        return PlayerWinLossRecords()
    # get_player_bio returns the overview url -> need to replace this
    url = BASE + player_bio.replace('/overview', '') + PLAYERS_WIN_LOSS_STATS
    soup = get_parsed_site_content(url)
    # start parsing
    tableContainer = soup.find('div', {'id': 'matchRecordTableContainer'})
    megaTables = tableContainer.select('.mega-table')
    for megaTable in megaTables:
        """
        I'm thinking everything under this can be a function
        I would call it with the Overall/Pressure Points/Envi...
        """
        thead_rows = megaTable.select('thead>th')
        tbody_rows = megaTable.select('tbody>tr')
        # if we are dealing with the Match Record sub table
        if any(th.text.strip() == 'Match Record' for th in thead_rows):
            match_record = {}
            for row in tbody_rows:
                tds = row.select('td')
                if any(td.text.strip() == 'Overall' for td in tds):
                    win_loss_stat= {}

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
                        if not inner_td.parent.parent.parent['class'][0] == 'inner-win-loss-cells':
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
                    print(win_loss_stat())








if __name__ == '__main__':
    print(get_player_win_loss_stats('RogerFederer'))
