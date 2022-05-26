from src.NCAABracketMaker import bracketmaker, compareResults
from src.NCAABracketMaker.utilities import simbracketpath
import os

try:
    testpath = (
        str(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")) + "/"
    )

except NameError:
    testpath = "tests/"


def test_brackets():
    league = 'mens'  # Must be 'mens' or 'womens'
    year = 2021  # Empty brackets available for 2021 and 2022 only

    win = 1.0  # Recommend: Float between 0 and 1
    rank = 1.0  # Recommend: Float between 0 and 1
    points = 1.0  # Recommend: Float between 0 and 1
    schedule = 1.0

    bracketmaker(league, year, win, rank, points, schedule)
    # Tests sim results match expected file
    assert compareResults(f'{testpath}testsim.csv',
                          f'{simbracketpath}{league}{year}-{win}-{rank}-{points}-{schedule}'
                          f'-Sim.csv') == 1, "Output changed from original algorithm"

