echo $PWD
TEST="$1"
case "$TEST" in
	# Win Loss test
	"wl")
		$PWD/venv/bin/python -m scraper.Tests PlayerParseTest.test_playerWinLoss
		;;
	"top_10")
	    $PWD/venv/bin/python -m scraper.Tests PlayerParseTest.test_playerWinLoss
		;;
	"titles")
		$PWD/venv/bin/python -m scraper.Tests PlayerParseTest.test_playerTitles
        ;;
	"")
		$PWD/venv/bin/python -m scraper.Tests
esac
