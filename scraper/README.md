# ATP Scraper

I noticed there is no reliable source of ATP information. I thought it would be good to write a web scraper that can provide this information.
So far, it:
- Can scrape a players overview page, grab their current ranking, ranking movement, prize money, win/loss, and titles for both singles and doubles.
- TODO:
	- <s>Decide how to split the code</s>
    - Parse the player's overall win/loss page for data.
	- Parse the titles page for a breakdown on titles won in each year
	- Parse the player's overall stats page for specific stats like career break point percentage
	- <s>Parse the player's ranking history</s>
	- Fix the error-handling -> return None or empty arrays/strings if an error is raised in lower functions
	- Decide if all this information should be included in one `Player` object
	    - Maybe add it to the players object when needed
