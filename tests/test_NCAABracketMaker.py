from src.NCAABracketMaker import bracketmaker, compareResults
from src.NCAABracketMaker.utilities import simbracketpath
import os

try:
    testpath = (
        str(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")) + "/TestDocs/"
    )

except NameError:
    testpath = "tests/TestDocs/"


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


# def test_inputs(caplog):
#     league = 'mens'  # Must be 'mens' or 'womens'
#     year = 2021  # Empty brackets available for 2021 and 2022 only
#
#     win = 1.0  # Recommend: Float between 0 and 1
#     rank = 1.0  # Recommend: Float between 0 and 1
#     points = 1.0  # Recommend: Float between 0 and 1
#     schedule = 1.0
#     # with pytest.raises(ValueError) as exc_info:
#     bracketmaker('Fish', year, win, rank, points, schedule)
#     out = caplog.text
#     assert out == 'Not a valid league. Must be either "mens" or "womens"\n'
#     # exception_raised = exc_info.value
#     # assert exception_raised == ValueError
#     # bracketmaker(league, year, win, rank, points, schedule)
