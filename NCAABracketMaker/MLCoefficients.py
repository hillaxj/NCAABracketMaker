from NCAABracketMaker.utilities import bracketpath, simbracketpath
import yaml
from NCAABracketMaker.AnalyzeGame import scheduleStrength
import numpy
import logging as log
import cProfile
from NCAABracketMaker.utilities import teampath
import time
import pandas as pd


def compareResults(results, simbracket):
    percentAccurate = 0
    # Imports yaml and converts to dict
    # with open(bracketpath + results) as f:
    #     dataResults = yaml.load(f, Loader=yaml.FullLoader)
    # with open(simbracketpath + simbracket) as f:
    #     dataSim = yaml.load(f, Loader=yaml.FullLoader)

    # Import files and converts to dict
    dataResults = pd.read_csv(results)
    dataSim = pd.read_csv(simbracket)

    # Increases percentAccurate if teams in each round match
    # Iterate through each round, skip first round teams
    for x in range(2, 8):
        # Iterates through each region
        for y in range(1, 5):
            seedid = f'd{x}r{y}seed'
            listResultsTeams = [v for k, v in dataResults.items() if k.startswith(seedid)]
            listSimTeams = [v for k, v in dataSim.items() if k.startswith(seedid)]
            # If element is in both lists, adds 1 to percentAccurate, perfect is 63 matching elements
            numAccurate = len([z for z in range(len(listResultsTeams)) if listResultsTeams[z] in listSimTeams])
            percentAccurate = percentAccurate + (numAccurate * pow(2, (x-2)))

    return percentAccurate / 192



# Below used for back testing ONLY
# Gets team data from web, run once ESPN has data from 2006 - current year
# Takes a long time to import data, ~10 min per year
# for x in range(2006, 2023):
#     getTeamData(league, x)

# Populate yaml/csv files from past brackets, run once CSV has data from 1985 - 2019
# for x in range(2006, 2023):
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
#     teamdatacsv = f'mens{x}.csv'
#     bracketresultsyaml = f'{x}results.yaml'
#     bracketSim(bracketresultsyaml, teamdatacsv)
#     compareList.append(compareYamls(bracketresultsyaml, f'mens{x}SimResults.yaml'))
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
# getTeamData(league, str(2022))
# bracketSim('NCAAMBracket2022.yaml', f'{league}{year}.csv', i, j, k, m)
# print(compareYamls(f'{year}results.yaml', f'{league}{year}-{i}-{j}-{k}-{m}-SimResults.csv'))
