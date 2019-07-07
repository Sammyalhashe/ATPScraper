class Ranking(object):
    """Ranking"""

    def __init__(self, date: str, singles: str, doubles: str):
        """__init__

        Rankings are returned as strings as they could be marked with
        a 'T' for 'tied'
        :param date: date the ranking was recorded
        :type date: str
        :param singles: singles ranking
        :type singles: str
        :param doubles: doubles ranking
        :type doubles: str
        """
        self.date = date
        self.singles = singles
        self.doubles = doubles
