from src.NCAABracketMaker import bracketmaker, compareResults
from src.NCAABracketMaker.utilities import simbracketpath


def test_brackets():
    league = 'mens'  # Must be 'mens' or 'womens'
    year = 2022  # Empty brackets available for 2021 and 2022 only

    win = 1  # Recommend: Float between 0 and 1
    rank = 1  # Recommend: Float between 0 and 1
    points = .5  # Recommend: Float between 0 and 1
    schedule = 5

    bracketmaker(league, year, win, rank, points, schedule)
    assert compareResults("test/testsim.csv", f'{simbracketpath}{league}{year}-{win}-{rank}-{points}-{schedule}-Sim.csv') \
           == 1, "Should be 1"

