TEST="$1"
case "$TEST" in
	# Win Loss test
	"wl")
		~/Documents/ATPScraper/ATPScraper/venv/bin/python -m scraper.Tests PlayerParseTest.test_playerWinLoss
		;;
	"top_10")
		~/Documents/ATPScraper/ATPScraper/venv/bin/python -m scraper.Tests PlayerParseTest.test_playerWinLoss
		;;
	"titles")
		~/Documents/ATPScraper/ATPScraper/venv/bin/python -m scraper.Tests PlayerParseTest.test_playerTitles
        ;;
	"")
		~/Documents/ATPScraper/ATPScraper/venv/bin/python -m scraper.Tests
esac
