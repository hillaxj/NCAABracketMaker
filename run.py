from TeamData import getTeamData, populateYAML
from BracketBuilder import bracketSim, populateBracket
from AnalyzeGame import scheduleStrength
from MLCoefficients import compareYamls
import numpy
import logging as log
from utilities import datapath
import pandas as pd
gender = 'mens'
league = 'college'
sport = 'basketball'
year = '2003'
averageAccuracy = 0
winWeight = 1  # Recommendation: Float between 0 and 1
rankWeight = 1  # Recommendation: Float between 0 and 1
pointsWeight = 1  # Recommendation: Float between 0 and 1
scheduleWeight = winWeight + rankWeight + pointsWeight  # Recommendation: Float between 1 and 3

# Gets team data from web, run once
# for x in range(int(year), 2021):
# getTeamData(gender, league, sport, str(2006))

# Populate yaml files from past brackets, run once
# for x in range(int(year), 2021):
#     populateYAML(x)

# for i in numpy.arange(0, 2, 0.25):
#     for j in numpy.arange(0, 2, 0.25):
#         for k in numpy.arange(0, 2, 0.25):
#             for m in numpy.arange(0.1, 4, 0.5):
i = 1
j = 1
k = 1
m = 1

compareList = []
# Calculate schedule strength, before bracketSim
log.info('scheduleStrength')
for x in range(int(year), 2020):
    scheduleStrength(gender + league + sport + str(x) + '.csv', i, j, k, m)

# Poorly simulate results based on starting 64 or 68 teams
log.info('bracketSim')
for x in range(int(year), 2020):
    bracketSim(str(x) + 'results.yaml', gender + league + sport + str(x) + '.csv')
log.info('compareYamls')
for x in range(int(year), 2020):
    compareList.append(compareYamls('2003results.yaml', 'menscollegebasketball2003SimResults.yaml'))
compareValue = sum(compareList) / len(compareList)

if compareValue > averageAccuracy:
    averageAccuracy = compareValue
    winWeight = i
    rankWeight = j
    pointsWeight = k
    scheduleWeight = m
    log.info(str(averageAccuracy) + ' ' + str(i) + ' ' + str(j) + ' ' + str(k) + ' ' + str(m))

print('Accuracy : ' + str(averageAccuracy))
print('winWeight : ' + str(winWeight))
print('rankWeight : ' + str(rankWeight))
print('pointWeight : ' + str(pointsWeight))
print('scheduleWeight : ' + str(scheduleWeight))


# Use to sim current year bracket
# bracketSim('NCAAMBracket2021.yaml', gender + league + sport + '2021' + '.csv')

# Doesn't work yet
# popBracket()
