from datetime import datetime, timedelta
from threading import Timer
from cachetools import LRUCache
from .constants import start_date

# think about adding a lock to the caches
ranking_history_cache = LRUCache(maxsize=128)
player_bio_cache = LRUCache(maxsize=128)
player_link_cache = LRUCache(maxsize=128)

caches = [player_bio_cache, player_link_cache, ranking_history_cache]

y = start_date.replace(
    day=start_date.day, hour=1, minute=0, second=0, microsecond=0) + timedelta(days=1)
delta_t = y - start_date

secs = delta_t.total_seconds()


def clear_caches():
    for cache in caches:
        cache.clear()


timer = Timer(secs, clear_caches)


def check_timer():
    if not timer.is_alive():
        timer.start()
