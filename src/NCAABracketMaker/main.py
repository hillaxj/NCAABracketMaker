"""
Call on functions to pull data and create brackets
"""
import logging

from src.NCAABracketMaker.BracketBuilder import clearSimResults, bracketSim, populateBracket
from src.NCAABracketMaker.TeamData import getTeamData, getemptybracket
from src.NCAABracketMaker.utilities import teampath, bracketpath
from os.path import exists


def bracketmaker(
    league: str,
    year: int,
    winWeight: float,
    rankWeight: float,
    pointsWeight: float,
    scheduleWeight: float,
    reset=False,
):
    """
    Imports data from current year and simulates bracket with defined parameters
    :param reset: bool, Default False, deletes all csv files in SimBrackets and clears results from Sim_Bracket.xlsx
    :param league: str, mens or womens
    :param year: int, year of bracket to test
    :param winWeight: float, number of wins weight coefficient
    :param rankWeight: float, top 25 team rank weight coefficient
    :param pointsWeight: float, points weight coefficient
    :param scheduleWeight: float, wins to losses weight coefficient
    :return: None, creates csv of team data and results, populates xlsx with results
    """
    if reset:
        # Removes all sim results
        clearSimResults(reset)
        logging.info("Cleared all simulation results")
        return None

    # Checks coefficient var types
    try:
        winWeight = float(winWeight)
        rankWeight = float(rankWeight)
        pointsWeight = float(pointsWeight)
        scheduleWeight = float(scheduleWeight)
    except ValueError:
        logging.error("Coefficients are not float variables", exc_info=True)
        return None

    # Checks league var type and converts to lower
    try:
        league = league.lower()
        if league == "mens":
            emptybracket = f"NCAAMBracket{year}.yaml"
        elif league == "womens":
            emptybracket = f"NCAAWBracket{year}.yaml"
        else:
            raise ValueError
    except ValueError:
        logging.error(
            'Not a valid league. Must be either "mens" or "womens"', exc_info=True
        )
        return None

    # Checks for empty bracket and generates one for only the current year if it doesn't exist
    if not exists(bracketpath + emptybracket):
        try:
            getemptybracket(league, year)
        except ValueError:
            return None

    # Checks for emptybracket again in case the selected year is not the current year
    if exists(bracketpath + emptybracket):
        # Gets team data from web, if file exist, doesn't run
        try:
            f = open(f"{teampath}{league}{year}.csv")
            f.close()
        except FileNotFoundError:
            getTeamData(league, year)

        # Use to sim current year bracket
        bracketSim(
            emptybracket,
            f"{league}{year}.csv",
            winWeight,
            rankWeight,
            pointsWeight,
            scheduleWeight,
        )
        # Generates Excel sheet with bracket results graphic
        populateBracket(
            f"{league}{year}-{winWeight}-{rankWeight}-{pointsWeight}-{scheduleWeight}-Sim.csv"
        )

        logging.info("Open Sim_Bracket.xlsx to see results.")
    else:
        logging.error("No empty bracket for selected year")

    return None
