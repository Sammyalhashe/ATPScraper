class Player:
    def __init__(self, name, bio_url=None):
        self.name = name
        self.bio = bio_url

    def set_bio(self, url):
        self.bio = url
