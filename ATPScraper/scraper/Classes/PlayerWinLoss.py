# class definition imports
from .WinLossStat import MatchRecord, PressurePoints, Environment, Other


class PlayerWinLossRecord(object):

    def __init__(self, match_record: MatchRecord=None, pressure_points: PressurePoints=None, environment: Environment=None, other: Other=None):
        self.match_record = match_record
        self.pressure_points = pressure_points
        self.environment = environment
        self.other = other

    def __call__(self):
        return {
            'match_record': self.match_record if not self.match_record else self.match_record(),
            'pressure_points': self.pressure_points if not self.pressure_points else self.pressure_points(),
            'environment': self.environment if not self.environment else self.environment(),
            'other': self.other if not self.other else self.otheer()
        }

    def set_match_record(self, mr: MatchRecord):
        if mr is not None:
            self.match_record = mr

    def set_pressure_points(self, pp: PressurePoints):
        if pp is not None:
            self.pressure_points = pp

    def set_environment(self, env: Environment):
        if env is not None:
            self.environment = env

    def set_other(self, other: Other):
        if other is not None:
            self.other = other


class PlayerWinLossRecords(object):

    def __init__(self, atp: PlayerWinLossRecord=None, challenger: PlayerWinLossRecord=None, itf: PlayerWinLossRecord=None):
        self.atp = atp
        self.challenger = challenger
        self.itf = itf 

    def __call__(self):
        return {
            'atp': self.atp if not self.atp else self.atp(),
            'challenger': self.challenger if not self.challenger else self.challenger(),
            'itf': self.itf if not self.itf else self.itf()
        }

    def set_atp(self, atp):
        if atp is not None:
            self.atp = atp

    def set_challenger(self, challenger):
        if challenger is not None:
            self.challenger = challenger

    def set_itf(self, itf):
        if itf is not None:
            self.itf = itf
