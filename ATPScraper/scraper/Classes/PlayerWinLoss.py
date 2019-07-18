# class definition imports
from .WinLossStat import MatchRecord, PressurePoints, Environment, Other


class PlayerWinLossRecord(object):
    """PlayerWinLossRecord"""

    def __init__(self,
                 MatchRecord: MatchRecord = None,
                 PressurePoints: PressurePoints = None,
                 Environment: Environment = None,
                 Other: Other = None):
        """__init__

        :param MatchRecord: MatchRecord stats
        :type MatchRecord: MatchRecord
        :param PressurePoints: PressurePoints stats
        :type PressurePoints: PressurePoints
        :param Environment: Environment stats (clay, hard, etc...)
        :type Environment: Environment
        :param Other: other stats
        :type Other: Other
        """
        self.match_record = MatchRecord
        self.pressure_points = PressurePoints
        self.environment = Environment
        self.other = Other

    def __call__(self):
        """__call__"""
        return {
            'match_record':
            self.match_record
            if not self.match_record else self.match_record(),
            'pressure_points':
            self.pressure_points
            if not self.pressure_points else self.pressure_points(),
            'environment':
            self.environment if not self.environment else self.environment(),
            'other':
            self.other if not self.other else self.other()
        }

    def isEmpty(self):
        """isEmpty"""
        return not self.match_record and \
            not self.pressure_points and \
            not self.environment and \
            not self.other

    def set_match_record(self, mr: MatchRecord):
        """set_match_record

        :param mr: match_record stats to set
        :type mr: MatchRecord
        """
        if mr is not None:
            self.match_record = mr

    def set_pressure_points(self, pp: PressurePoints):
        """set_pressure_points

        :param pp: pressure_points stats to set
        :type pp: PressurePoints
        """
        if pp is not None:
            self.pressure_points = pp

    def set_environment(self, env: Environment):
        """set_environment

        :param env: environment stats to set
        :type env: Environment
        """
        if env is not None:
            self.environment = env

    def set_other(self, other: Other):
        """set_other

        :param other: other stats to set
        :type other: Other
        """
        if other is not None:
            self.other = other


class PlayerWinLossRecords(object):
    """PlayerWinLossRecords"""

    def __init__(self,
                 tour: PlayerWinLossRecord = None,
                 challenger: PlayerWinLossRecord = None,
                 itf: PlayerWinLossRecord = None):
        """__init__

        :param tour: PlayerWinLossRecord on atp tour
        :type tour: PlayerWinLossRecord
        :param challenger: PlayerWinLossRecord on challenger tour
        :type challenger: PlayerWinLossRecord
        :param itf: PlayerWinLossRecord on itf tour
        :type itf: PlayerWinLossRecord
        """
        self.tour = tour
        self.challenger = challenger
        self.itf = itf

    def __call__(self):
        """__call__"""
        return {
            'tour':
            self.tour if not self.tour else self.tour(),
            'challenger':
            self.challenger if not self.challenger else self.challenger(),
            'itf':
            self.itf if not self.itf else self.itf()
        }

    def set_atp(self, atp: PlayerWinLossRecord):
        """set_atp

        :param atp: set the atp tour PlayerWinLossRecord
        :type atp: PlayerWinLossRecord
        """
        if atp is not None:
            self.tour = atp

    def set_challenger(self, challenger: PlayerWinLossRecord):
        """set_challenger

        :param challenger: set the challenger tour PlayerWinLossRecord
        :type challenger: PlayerWinLossRecord
        """
        if challenger is not None:
            self.challenger = challenger

    def set_itf(self, itf: PlayerWinLossRecord):
        """set_itf

        :param itf: set the itf tour PlayerWinLossRecord
        :type itf: PlayerWinLossRecord
        """
        if itf is not None:
            self.itf = itf
