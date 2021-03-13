from TeamData import getTeamData, populateYAML
from BracketBuilder import bracketSim, populateBracket
from AnalyzeGame import scheduleStrength
from utilities import datapath
import pandas as pd
gender = 'mens'
league = 'college'
sport = 'basketball'
year = '2003'
winWeight = 1  # Recommendation: Float between 0 and 1
rankWeight = 1  # Recommendation: Float between 0 and 1
pointsWeight = 1  # Recommendation: Float between 0 and 1
scheduleWeight = winWeight + rankWeight + pointsWeight  # Recommendation: Float between 1 and 3

# Calculate schedule strength
# for x in range(int(year), 2021):
#     #     getTeamData(gender, league, sport, '2014')
#     scheduleStrength(gender + league + sport + year + '.csv', winWeight, rankWeight, pointsWeight, scheduleWeight)

# Populate yaml files from past brackets
# for x in range(int(year), 2021):
#     populateYAML(x)

# Poorly simulate results based on starting 64 or 68 teams
for x in range(int(year), 2021):
    print(x)
    bracketSim(str(x) + 'results.yaml', gender + league + sport + str(x) + '.csv')

bracketSim('NCAAMBracket2021.yaml', gender + league + sport + '2021' + '.csv')
# popBracket()



# print()