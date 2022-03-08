from NCAABracketMaker.utilities import bracketpath, simbracketpath
import yaml
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
