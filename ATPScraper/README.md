# ATP Scraper

I noticed there is no reliable source of ATP information. I thought it would be good to write a web scraper that can provide this information.
So far, it:
- Can scrape a players overview page, grab their current ranking, ranking movement, prize money, win/loss, and titles for both singles and doubles.
- TODO:
	- <s>Decide how to split the code</s>
    - <s>Parse the player's overall win/loss page for data.</s>
	- <s>Look into server cacheing: https://github.com/tkem/cachetools/blob/master/cachetools/ttl.py </s>
	- <s>Parse the titles page for a breakdown on titles won in each year</s>
		- Remove from this endpoint parsing the tournament url
		- it's better to just provide the parsed name of the tournament and the url
		- Add endpoint to parse tournament overview with url fragment
	- <s>Parse the player's overall stats page for specific stats like career break point percentage</s>
	- <s>Parse the player's ranking history</s>
	- <s>Fix the error-handling -> return None or empty arrays/strings if an error is raised in lower functions</s>
	- <s>Decide if all this information should be included in one `Player` object</s>
	    - <s>Maybe add it to the players object when needed</s>
