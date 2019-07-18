from collections import namedtuple
from typing import List


class Tournament(object):
    def __init__(self,
                 name: str = None,
                 surface: str = None,
                 level: str = None,
                 bio: str = None,
                 draw_size: List[int] = None,
                 prize_money: str = None,
                 total_financial_commitment: str = None):
        self.name = name
        self.surface = surface
        self.bio = bio
        self.level = level
        self.draw_size = draw_size
        self.prize_money = prize_money
        self.total_financial_commitment = total_financial_commitment

    def __call__(self):
        return {
            'name': self.name,
            'surface': self.surface,
            'bio': self.bio,
            'level': self.level,
            'draw_size': self.draw_size,
            'prize_money': self.prize_money,
            'total_financial_commitment': self.total_financial_commitment
        }


Tournaments = List[Tournament]


class TitlesYear(object):
    def __init__(self, year: int, titles: int, finals: int,
                 tournaments: Tournaments):
        self.year = year
        self.titles = titles
        self.finals = finals
        self.tournaments = tournaments

    def __call__(self):
        return {
            'year': self.year,
            'titles': self.titles,
            'finals': self.finals,
            'tournaments': self.tournaments
        }


TitleYearList = List[TitlesYear]


class TitleList(TitleYearList):
    def __init__(self):
        self = []

    def __add__(self, newVal):
        self.append(newVal)

    def setTitleList(self, titleList):
        self = titleList
