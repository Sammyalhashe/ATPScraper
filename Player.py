class Player:
    def __init__(self, name, current_year_stats, career_stats, bio_url=None):
        self.name = name
        self.bio = bio_url
        self.cy_stats = current_year_stats
        self.career_stats = career_stats

    def set_bio(self, url):
        self.bio = url
