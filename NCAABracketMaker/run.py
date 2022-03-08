from NCAABracketMaker.TeamData import getTeamData, populateResults
from NCAABracketMaker.BracketBuilder import bracketSim, populateBracket
from NCAABracketMaker.AnalyzeGame import scheduleStrength
from NCAABracketMaker.MLCoefficients import compareResults
import numpy
import logging as log
import cProfile
from NCAABracketMaker.utilities import teampath
import time
import pandas as pd
gender = 'mens'
league = 'college'
sport = 'basketball'
year = 2021
averageAccuracy = 0
winWeight = 1  # Recommendation: Float between 0 and 1
rankWeight = 1.1 # Recommendation: Float between 0 and 1
pointsWeight = 1  # Recommendation: Float between 0 and 1
scheduleWeight = 1  # Recommendation: Float between 1 and 3
i = winWeight
j = rankWeight
k = pointsWeight
m = scheduleWeight


# Gets team data from web, run once
# for x in range(year, 2006):
#     getTeamData(gender, league, sport, x)


# Populate yaml files from past brackets, run once
# for x in range(year, 2022):
#     populateResults(x)

# increment = 0.25
# for i in numpy.arange(1.2, 2.5, .1):
#     for j in numpy.arange(1.2, 2.5, .1):
#         # for k in numpy.arange(0, 1.3, .1):
#         # for m in numpy.arange(.8, 2.5, .1):
# compareList = []
# # Calculate schedule strength, before bracketSim
# log.info(f'NextSim {i} {j} {k} {m}')
# scheduleWeight = i + j +  0.0001
#
# for x in range(year, 2020):
#     teamdatacsv = f'menscollegebasketball{x}.csv'
#     bracketresultsyaml = f'{x}results.yaml'
#     bracketSim(bracketresultsyaml, teamdatacsv)
#     compareList.append(compareYamls(bracketresultsyaml, f'menscollegebasketball{x}SimResults.yaml'))
#
# compareValue = sum(compareList) / len(compareList)
# print(compareValue)
# # Poorly simulate results based on starting 64 or 68 teams
# if compareValue > averageAccuracy:
#     averageAccuracy = compareValue
#     winWeight = i
#     rankWeight = j
#     pointsWeight = k
#     scheduleWeight = m
#     log.info(f'{averageAccuracy} {i} {j} {k} {m}')
#
# print('Accuracy : ' + str(averageAccuracy))
# print('winWeight : ' + str(winWeight))
# print('rankWeight : ' + str(rankWeight))
# print('pointWeight : ' + str(pointsWeight))
# print('scheduleWeight : ' + str(scheduleWeight))


# Use to sim current year bracket
# getTeamData(gender, league, sport, str(2021))
bracketSim('NCAAMBracket2021.csv', f'{gender}{league}{sport}{year}.csv', i, j, k, m)
# print(compareYamls(f'{year}results.yaml', f'{gender}{league}{sport}{year}-{i}-{j}-{k}-{m}-SimResults.csv'))

# Doesn't work yet
populateBracket(f'{gender}{league}{sport}{year}-{i}-{j}-{k}-{m}-SimResults.csv')
