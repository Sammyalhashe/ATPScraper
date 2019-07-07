from .Utils import get_site_content

RANKINGS = "https://www.atptour.com/en/rankings/singles"
FEDERER = "https://www.atptour.com/en/players/roger-federer/f324/overview"
RANKING_HISTORY = "https://www.atptour.com/en/players/roger-federer/f324/rankings-history"
WIN_LOSS = "https://www.atptour.com/en/players/roger-federer/f324/fedex-atp-win-loss"
TITLES_FINALS = "https://www.atptour.com/en/players/roger-federer/f324/titles-and-finals"
STATS = "https://www.atptour.com/en/players/roger-federer/f324/player-stats?year=0&surfaceType=all"

urls = [RANKINGS, FEDERER, RANKING_HISTORY, WIN_LOSS, TITLES_FINALS, STATS]
names = [
    'rankings', 'federer', 'rankings-history', 'win-loss', 'titles-and-finals',
    'stats'
]

for url, name in zip(urls, names):
    with open('./' + name + '.txt', 'w') as f:
        asdf = get_site_content(url)
        f.writelines(str(asdf))
