class Player:
    def __init__(self, name, current_year_stats, career_stats, bio_url=None):
        self.name = name
        self.bio = bio_url
        self.cy_stats = current_year_stats
        self.career_stats = career_stats

    def __str__(self):
        player_string = "\n-------------------------\n"
        player_string += "Player name: {}\n".format(self.name)
        player_string += "Player bio: {}\n".format(self.bio)
        for stat in self.cy_stats:
            player_string += "{0}: {1}\n".format(stat, self.cy_stats[stat])
        for stat in self.career_stats:
            player_string += "{0}: {1}\n".format(stat, self.career_stats[stat])
        player_string = "-------------------------\n"
        return player_string

    def set_bio(self, url):
        self.bio = url
