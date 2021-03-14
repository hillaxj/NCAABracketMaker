from TeamData import getTeamData, populateYAML
from BracketBuilder import bracketSim, populateBracket
from AnalyzeGame import scheduleStrength
from MLCoefficients import compareYamls
import numpy
import logging as log
import cProfile
from utilities import datapath
import pandas as pd
gender = 'mens'
league = 'college'
sport = 'basketball'
year = '2003'
averageAccuracy = 0
winWeight = 1 # Recommendation: Float between 0 and 1
rankWeight = 1.1  # Recommendation: Float between 0 and 1
pointsWeight = 0  # Recommendation: Float between 0 and 1
scheduleWeight = 1  # Recommendation: Float between 1 and 3
i = winWeight
j = rankWeight
k = pointsWeight
m = scheduleWeight


# Gets team data from web, run once
# for x in range(int(year), 2021):
# getTeamData(gender, league, sport, str(2006))

# Populate yaml files from past brackets, run once
for x in range(int(2020), 2022):
    populateYAML(x)
# increment = 0.25
# # for i in numpy.arange(.9, 1.2, .01):
# #     for j in numpy.arange(.9, 1.2, .01):
# #         # for k in numpy.arange(0, 2, .1):
# #         for m in numpy.arange(.9, 1.2, .01):
# compareList = []
# # Calculate schedule strength, before bracketSim
# log.info(f'NextSim {i} {j} {k} {m}')
# # scheduleWeight = i + j +  0.0001
#
# for x in range(int(year), 2020):
#     teamdatacsv = f'menscollegebasketball{x}.csv'
#     bracketresultsyaml = f'{x}results.yaml'
#     scheduleStrength(teamdatacsv, i, j, 0, m)
#     bracketSim(bracketresultsyaml, teamdatacsv)
#     compareList.append(compareYamls(bracketresultsyaml, f'menscollegebasketball{x}SimResults.yaml'))
#
# compareValue = sum(compareList) / len(compareList)
# # Poorly simulate results based on starting 64 or 68 teams
# if compareValue > averageAccuracy:
#     averageAccuracy = compareValue
#     winWeight = i
#     rankWeight = j
#     pointsWeight = 0
#     scheduleWeight = m
#     log.info(f'{averageAccuracy} {i} {j} 0 {m}')
#     # + ' ' + str(m))
#
# print('Accuracy : ' + str(averageAccuracy))
# print('winWeight : ' + str(winWeight))
# print('rankWeight : ' + str(rankWeight))
# print('pointWeight : ' + str(pointsWeight))
# print('scheduleWeight : ' + str(scheduleWeight))


# Use to sim current year bracket
bracketSim('NCAAMBracket2021.yaml', gender + league + sport + '2021' + '.csv')

# Doesn't work yet
# popBracket()
