"""
Call on functions to pull data and create brackets
"""
from NCAABracketMaker.TeamData import getTeamData
from NCAABracketMaker.BracketBuilder import bracketSim, populateBracket

gender = 'mens'
year = 2022

winWeight = 1       # Recommend: Float between 0 and 1
rankWeight = 1.5    # Recommend: Float between 0 and 1
pointsWeight = 1    # Recommend: Float between 0 and 1
scheduleWeight = 3  # Recommend: Float between 1 and 3


# Gets team data from web, run once for current year
getTeamData(gender, 2022)

# Use to sim current year bracket
if gender == 'mens':
    bracketSim(f'NCAAMBracket{year}.yaml', f'{gender}{year}.csv', winWeight, rankWeight, pointsWeight, scheduleWeight)
elif gender == 'womens':
    bracketSim(f'NCAAWBracket{year}.yaml', f'{gender}{year}.csv', winWeight, rankWeight, pointsWeight, scheduleWeight)

# Generates Excel sheet with bracket results graphic
# Open Sim_Bracket.xlsx in SimBrackets to view results
populateBracket(f'{gender}{year}-{winWeight}-{rankWeight}-{pointsWeight}-{scheduleWeight}-Sim.csv')




