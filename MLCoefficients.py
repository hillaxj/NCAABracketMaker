from utilities import bracketpath, simbracketpath
import yaml


def compareYamls(resultsyaml, simbracketyaml):
    percentAccurate = 0
    # Imports yaml and converts to dict
    with open(bracketpath + resultsyaml) as f:
        dataResultsYaml = yaml.load(f, Loader=yaml.FullLoader)
    with open(simbracketpath + simbracketyaml) as f:
        dataSimYaml = yaml.load(f, Loader=yaml.FullLoader)

    # Increases percentAccurate if teams in each round match
    # Iterate through each round, skip first round teams
    for x in range(2, 8):
        # Iterates through each region
        for y in range(1, 5):
            listResultsTeams = [v for k, v in dataResultsYaml.items() if k.startswith('d'+ str(x)+'r'+str(y)+'seed')]
            listSimTeams = [v for k, v in dataSimYaml.items() if k.startswith('d' + str(x) + 'r' + str(y) + 'seed')]
            # If element is in both lists, adds 1 to percentAccurate, perfect is 63 matching elements
            for z in range(len(listResultsTeams)):
                if listResultsTeams[z] in listSimTeams:
                    percentAccurate = percentAccurate + 1

    return percentAccurate / 63
