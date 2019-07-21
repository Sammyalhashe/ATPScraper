# ATP Scraper

I noticed there is no reliable source of ATP information. I thought it would be good to write a web scraper that can provide this information.
So far, it:

- Can scrape a players overview page, grab their current ranking, ranking movement, prize money, win/loss, and titles for both singles and doubles.
- Fun fact: ATP website is created with Vue.js

## TODO:

- <s>Decide how to split the code</s>
  - <s>Parse the player's overall win/loss page for data.</s>
- <s>Look into server cacheing: https://github.com/tkem/cachetools/blob/master/cachetools/ttl.py </s>
- <s>Parse the titles page for a breakdown on titles won in each year</s>
- <s>Remove from this endpoint parsing the tournament url</s>
- <s>it's better to just provide the parsed name of the tournament and the url</s>
- <s>Add endpoint to parse tournament overview with url fragment</s>
- <s>Parse the player's overall stats page for specific stats like career break point percentage</s>
- <s>Parse the player's ranking history</s>
- <s>Fix the error-handling -> return None or empty arrays/strings if an error is raised in lower functions</s>
- <s>Decide if all this information should be included in one `Player` object</s>
  - <s>Maybe add it to the players object when needed</s>
- <s>Fix the doubles title parsing to include doubles player issue</s>
- Maybe add endpoint to search by player by url just like tournament overview
- Add way to parse a range of dates for ranking history endpoint
- <s>Deploy intial version with docs</s>

## Endpoints:

`/api/top_10` -> get's top 10 players (maybe extend to top n?)

`/api/tournament_overview/{tournament_name || name: tournament_id}?{url=False}` -> parses tournament overview page by by searching for the name of the tournament if `url` is set `False` else uses a fragment of the tournaments url to search if `url` is `True`. For example, the url of Halle is "/en/tournaments/halle/500/overview", if `url` is set to `True`, put `halle:500`

`/api/player_overview/{player_name}` -> searches for player name, and returns a player overview

`/api/{player_name}/titles?{years="*"}` -> finds the titles (and finals) `player_name` has won in his career. If the query `years="*"`, which is the default, it finds all the titles for all the years recorded. You _can_ choose the years for the player however, simply choose them by specifying a **comma-separated** group of years in the `year` query parameter. For example: `/api/RogerFederer/titles?years=2019,2017,2001,2000`

`/api/player_win_loss/{player_name}?{tour="*"}` -> finds all the stats regarding wins and losses in both the current year and career in general. By default, it parses all tour types, but you can specify a `tour` type that is one of `{'tour', 'challenger', 'itf'}`

`/api/ranking_history/{player_name}` -> returns the ranking history for `plyaer_name`
