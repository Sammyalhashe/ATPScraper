from typing import List


class WinLossStat(object):
    """WinLossStat"""

    def __init__(self,
                 ytd_wl: List[int],
                 ytd_fedex: float,
                 car_wl: List[int],
                 car_fedex: float,
                 titles: int = None):
        """__init__

        :param ytd_wl:
        :type ytd_wl: List[int], ytd_fedex
        :param car_fedex:
        :type car_fedex: float
        :param titles:
        :type titles: int
        """
        self.ytd_wl = ytd_wl
        self.ytd_fedex = ytd_fedex
        self.car_wl = car_wl
        self.car_fedex = car_fedex
        self.titles = titles

    def __call__(self):
        """__call__"""
        return {
            'ytd_wl': self.ytd_wl,
            'ytd_fedex': self.ytd_fedex,
            'car_wl': self.car_wl,
            'car_fedex': self.car_fedex,
            'titles': self.titles
        }


WL = WinLossStat


class MatchRecord(object):
    """MatchRecord"""

    def __init__(self,
                 overall: WL,
                 grand_slams: WL = None,
                 atp_masters_1000: WL = None):
        """__init__

        :param overall:
        :type overall: WL
        :param grand_slams:
        :type grand_slams: WL
        :param atp_masters_1000:
        :type atp_masters_1000: WL
        """
        self.overall = overall
        self.grand_slams = grand_slams
        self.atp_masters_1000 = atp_masters_1000

    def __call__(self):
        """__call__"""
        return {
            'overall':
            self.overall(),
            'grand_slams':
            self.grand_slams if not self.grand_slams else self.grand_slams(),
            'atp_masters_1000':
            self.atp_masters_1000
            if not self.atp_masters_1000 else self.atp_masters_1000()
        }


class PressurePoints(object):
    """PressurePoints"""

    def __init__(self,
                 tiebreaks: WL,
                 finals: WL,
                 versus_top_10: WL = None,
                 deciding_set_3rd_or_5th_set: WL = None,
                 _5th_set_record: WL = None):
        """__init__

        :param tiebreaks:
        :type tiebreaks: WL
        :param finals:
        :type finals: WL
        :param versus_top_10:
        :type versus_top_10: WL
        :param deciding_set_3rd_or_5th_set:
        :type deciding_set_3rd_or_5th_set: WL
        :param _5th_set_record:
        :type _5th_set_record: WL
        """
        self.tiebreaks = tiebreaks
        self.versus_top_10 = versus_top_10
        self.finals = finals
        self.deciding_set_3rd_or_5th_set = deciding_set_3rd_or_5th_set
        self._5th_set_record = _5th_set_record

    def __call__(self):
        """__call__"""
        return {
            'tiebreaks':
            self.tiebreaks(),
            'versus_top_10':
            self.versus_top_10
            if not self.versus_top_10 else self.versus_top_10(),
            'finals':
            self.finals(),
            'deciding_set_3rd_or_fifth':
            self.deciding_set_3rd_or_5th_set
            if not self.deciding_set_3rd_or_5th_set else
            self.deciding_set_3rd_or_5th_set(),
            '_5th_set_record':
            self._5th_set_record
            if not self._5th_set_record else self._5th_set_record()
        }


class Environment(object):
    """Environment"""

    def __init__(self,
                 clay: WL,
                 grass: WL,
                 hard: WL,
                 indoor: WL,
                 outdoor: WL,
                 carpet: WL = None):
        """__init__

        :param clay:
        :type clay: WL
        :param grass:
        :type grass: WL
        :param hard:
        :type hard: WL
        :param indoor:
        :type indoor: WL
        :param outdoor:
        :type outdoor: WL
        :param carpet:
        :type carpet: WL
        """
        self.clay = clay
        self.grass = grass
        self.hard = hard
        self.indoor = indoor
        self.outdoor = outdoor
        self.carpet = carpet

    def __call__(self):
        """__call__"""
        return {
            'clay': self.clay(),
            'grass': self.grass(),
            'hard': self.hard(),
            'indoor': self.indoor(),
            'outdoor': self.outdoor(),
            'carpet': self.carpet if not self.carpet else self.carpet()
        }


class Other(object):
    """Other"""

    def __init__(self,
                 vs_right_handers: WL,
                 vs_left_handers: WL,
                 after_winning_1st_set: WL = None,
                 after_losing_1st_set: WL = None):
        """__init__

        :param vs_right_handers:
        :type vs_right_handers: WL
        :param vs_left_handers:
        :type vs_left_handers: WL
        :param after_winning_1st_set:
        :type after_winning_1st_set: WL
        :param after_losing_1st_set:
        :type after_losing_1st_set: WL
        """
        self.after_winning_1st_set = after_winning_1st_set
        self.after_losing_1st_set = after_losing_1st_set
        self.vs_right_handers = vs_right_handers
        self.vs_left_handers = vs_left_handers

    def __call__(self):
        """__call__"""
        return {
            'after_winning_1st_set':
            self.after_winning_1st_set if not self.after_winning_1st_set else
            self.after_winning_1st_set(),
            'after_losing_1st_set':
            self.after_losing_1st_set
            if not self.after_losing_1st_set else self.after_losing_1st_set(),
            'vs_right_handers':
            self.vs_right_handers(),
            'vs_left_handers':
            self.vs_left_handers()
        }
