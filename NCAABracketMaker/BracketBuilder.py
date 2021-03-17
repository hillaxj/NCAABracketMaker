from NCAABracketMaker.utilities import bracketpath, simbracketpath, datapath, modulepath
import yaml
from NCAABracketMaker.AnalyzeGame import whoWins
from math import pow
import PyPDF2
import pandas as pd
import os


def roundResults(teams, round, teamdatadf):
    # Tests each game for defined round
    winners = {}

    # Loops through each game by region

    for x in range(1, 5):
        for y in range(1, int(pow(2, 4-round) + 1)):
            seedid = f'd{round}r{x}seed'
            winners[f'd{round+1}r{x}seed{y}'] = whoWins(teams.get(''.join([seedid, str(y)])), \
                                            teams.get(''.join([seedid, str(int(pow(2, 5-round) + 1-y))])), teamdatadf)

    return winners


def bracketSim(bracketfile, teamdatafile):
    if '2020' in bracketfile:
        with open(simbracketpath + teamdatafile.replace('.csv', '') + 'SimResults.yaml', 'w') as f:
            yaml.dump('Coronavirus', f, default_flow_style=False)
        print('Coronavirus')
        return None

    teamdatadf = pd.read_csv(datapath + teamdatafile, index_col='Team Name')
    # Simulates all games in the supplied brackets based on teamdatafile info
    with open(bracketpath + bracketfile) as f:
        dataYaml = yaml.load(f, Loader=yaml.FullLoader)

    data = dict((k, v) for k, v in dataYaml.items() if k[:2] == 'd1')

    # First 4 games
    try:
        data['d1r1seed16'] = whoWins(data.get('d1r1seed16a'), data.get('d1r1seed16b'), teamdatadf)
        data['d1r1seed11'] = whoWins(data.get('d1r1seed11a'), data.get('d1r1seed11b'), teamdatadf)
        data['d1r4seed16'] = whoWins(data.get('d1r4seed16a'), data.get('d1r4seed16b'), teamdatadf)
        data['d1r4seed11'] = whoWins(data.get('d1r4seed11a'), data.get('d1r4seed11b'), teamdatadf)

    except:
        pass

    # Simulates and stores each round until winner is determined
    champion = {}
    round1winners = roundResults(data, 1, teamdatadf)
    round2winners = roundResults(round1winners, 2, teamdatadf)
    round3winners = roundResults(round2winners, 3, teamdatadf)
    round4winners = roundResults(round3winners, 4, teamdatadf)
    round5winners = {'d6r1seed1': whoWins(round4winners.get('d5r1seed1'), round4winners.get('d5r4seed1'), teamdatadf), \
                     'd6r1seed2': whoWins(round4winners.get('d5r2seed1'), round4winners.get('d5r3seed1'), teamdatadf)}
    champion['d7r1seed1'] = whoWins(round5winners.get('d6r1seed1'), round5winners.get('d6r1seed2'), teamdatadf)

    try:
        data.pop('d1r1seed16a')
        data.pop('d1r1seed16b')
        data.pop('d1r1seed12a')
        data.pop('d1r1seed12b')
        data.pop('d1r4seed16a')
        data.pop('d1r4seed16b')
        data.pop('d1r4seed12a')
        data.pop('d1r4seed12b')
    except:
        pass

    totalsimData = {**data, **round1winners, **round2winners, **round3winners, **round4winners, **round5winners, **champion}

    # ensure directory exists
    os.makedirs(modulepath + 'SimBrackets/', exist_ok=True)
    with open(simbracketpath + teamdatafile.replace('.csv', '') + 'SimResults.yaml', 'w') as f:
        yaml.dump(totalsimData, f, default_flow_style=False)

    return None


def populateBracket():

    pdf = open(bracketpath + 'NCAA Bracket clean.pdf')
    readpdf = PyPDF2.PdfFileReader(pdf)



    return None
