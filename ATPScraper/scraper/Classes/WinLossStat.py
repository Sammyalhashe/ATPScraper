from typing import List


class WinLossStat(object):

    def __init__(self, ytd_wl: List[int], ytd_fedex: float, car_wl: List[int], car_fedex: float, titles: int=None):
        self.ytd_wl = ytd_wl
        self.ytd_fedex = ytd_fedex
        self.car_wl = car_wl
        self.car_fedex = car_fedex
        self.titles = titles


    def __call__(self):
        return {
            'ytd_wl': self.ytd_wl,
            'ytd_fedex': self.ytd_fedex,
            'car_wl': self.car_wl,
            'car_fedex': self.car_fedex,
            'titles': self.titles
        }

WL = WinLossStat

class MatchRecord(object):

    def __init__(self, overall: WL, grand_slams: WL, masters: WL):
        self.overall = overall
        self.grand_slams = grand_slams
        self.masters = masters

    def __call__(self):
        return {
            'overall': self.overall(),
            'grand_slams': self.grand_slams(),
            'masters': self.masters()
        }

class PressurePoints(object):

    def __init__(self, tiebreaks: WL, v_top10: WL, finals: WL, dec_set: WL, set_5_rec: WL):
        self.tiebreaks = tiebreaks
        self.v_top10 = v_top10,
        self.finals = finals
        self.dec_set = dec_set
        self.set_5_rec = set_5_rec

    def __call__(self):
        return {
            'tiebreaks': self.tiebreaks(),
            'v_top10': self.v_top10(),
            'finals': self.finals(),
            'dec_set': self.dec_set(),
            'set_5_rec': self.set_5_rec()
        }


class Environment(object):

    def __init__(self, clay: WL, grass: WL, hard: WL, indoor: WL, outdoor: WL, carpet: WL=None):
        self.clay = clay
        self.grass = grass
        self.hard = hard
        self.indoor = indoor
        self.outdoor = outdoor,
        self.carpet = carpet

    def __call__(self):
        return {
            'clay': self.clay(),
            'grass': self.grass(),
            'hard': self.hard(),
            'indoor': self.indoor(),
            'outdoor': self.outdoor(),
            'carpet': self.carpet if not self.carpet else self.carpet()
        }


class Other(object):

    def __init__(self, after_win_first: WL, after_lose_first: WL, v_right_handers: WL, v_left_handers: WL):
        self.after_win_first = after_win_first
        self.after_lose_first = after_lose_first
        self.v_right_handers = v_right_handers
        self.v_left_handers = v_left_handers

    def __call__(self):
        return {
            'after_win_first': self.after_win_first(),
            'after_lose_first': self.after_lose_first(),
            'v_right_handers': self.v_right_handers(),
            'v_left_handers': self.v_left_handers()
        }
