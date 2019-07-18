from datetime import datetime, timedelta
from threading import Timer
from cachetools import LRUCache, TTLCache
from .constants import start_date

# think about adding a lock to the caches
ranking_history_cache = TTLCache(maxsize=128, ttl=86400)
player_bio_cache = TTLCache(maxsize=128, ttl=86400)
player_link_cache = LRUCache(maxsize=128)
player_win_loss_cache = TTLCache(maxsize=128, ttl=86400)
player_titles_finals_cache = TTLCache(maxsize=128, ttl=86400)
tournament_overview_cache = TTLCache(maxsize=128, ttl=86400)

caches = [player_bio_cache, player_link_cache, ranking_history_cache]

y = start_date.replace(
    day=start_date.day, hour=1, minute=0, second=0, microsecond=0) + timedelta(days=1)
delta_t = y - start_date

secs = delta_t.total_seconds()


def clear_caches():
    for cache in caches:
        cache.clear()



class RepeatableTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = function
        self._args = args
        self._kwargs = kwargs

    def start(self):
        t = Timer(self.interval, self.function, self._args, self._kwargs)
        t.start()

timer = None

def check_timer():
    global timer
    if not timer:
        timer = Timer(secs, clear_caches)
    if not timer.is_alive():
        timer.start()
