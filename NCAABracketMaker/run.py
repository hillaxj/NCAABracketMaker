"""
Call on functions to pull data and create brackets
"""
from NCAABracketMaker.BracketBuilder import bracketmaker


sex = 'mens'        # Must be 'mens' or 'womens'
year = 2022         # Empty brackets available for 2021 and 2022 only

win = 1             # Recommend: Float between 0 and 1
rank = .2           # Recommend: Float between 0 and 1
points = 1          # Recommend: Float between 0 and 1
schedule = 5        # Recommend: Float between 1 and 3

reset = False

# Imports data from current year and simulates bracket with defined parameters. Open Sim_Bracket.xlsx to see results.
bracketmaker(sex, year, win, rank, points, schedule)







