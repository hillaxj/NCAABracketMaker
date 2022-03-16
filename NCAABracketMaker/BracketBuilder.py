from NCAABracketMaker.utilities import bracketpath, simbracketpath, teampath, modulepath
import yaml
from NCAABracketMaker.AnalyzeGame import whoWins
from math import pow
import pandas as pd
import os
from openpyxl import load_workbook
# TODO : Add function to import current year bracket into yaml ie: NCAAMBracket2021.yaml

def roundResults(teams, round, teamdatadf, pointcof, wincof, rankcof, ratiocof):
    # Tests each game for defined round
    winners = {}

    # Loops through each game by region

    for x in range(1, 5):
        for y in range(1, int(pow(2, 4-round) + 1)):
            seedid = f'd{round}r{x}seed'
            winners[f'd{round+1}r{x}seed{y}'] = whoWins(teams.get(''.join([seedid, str(y)])),
                                            teams.get(''.join([seedid, str(int(pow(2, 5-round) + 1-y))])), teamdatadf, pointcof, wincof, rankcof, ratiocof)

    return winners


def bracketSim(bracketfile, teamdatafile, pointcof, wincof, rankcof, ratiocof):
    if '2020' in bracketfile:
        # with open(simbracketpath + teamdatafile.replace('.csv', '') + 'Sim.yaml', 'w') as f:
        #     yaml.dump('Coronavirus', f, default_flow_style=False)
        with open(simbracketpath + teamdatafile.replace('.csv', '') + 'Sim.csv', 'w') as f:
            f.write('Coronavirus')
        print('Coronavirus')
        return None

    teamdatadf = pd.read_csv(teampath + teamdatafile, index_col='Team Name')
    # Simulates all games in the supplied brackets based on teamdatafile info
    with open(bracketpath + bracketfile) as f:
        bracketData = yaml.load(f, Loader=yaml.FullLoader)
    # bracketData = pd.read_csv(bracketpath + bracketfile)

    data = dict((k, v) for k, v in bracketData.items() if k[:2] == 'd1')

    # First 4 games, different years have different first 4 games
    try:
        data['d1r1seed16'] = whoWins(data.get('d1r1seed16a'), data.get('d1r1seed16b'), teamdatadf, pointcof, wincof, rankcof, ratiocof)
    except:
        pass
    try:
        data['d1r1seed11'] = whoWins(data.get('d1r1seed11a'), data.get('d1r1seed11b'), teamdatadf, pointcof, wincof, rankcof, ratiocof)
    except:
        pass
    try:
        data['d1r2seed16'] = whoWins(data.get('d1r2seed16a'), data.get('d1r2seed16b'), teamdatadf, pointcof, wincof, rankcof, ratiocof)
    except:
        pass
    try:
        data['d1r2seed11'] = whoWins(data.get('d1r2seed11a'), data.get('d1r2seed11b'), teamdatadf, pointcof, wincof, rankcof, ratiocof)
    except:
        pass
    try:
        data['d1r3seed16'] = whoWins(data.get('d1r3seed16a'), data.get('d1r3seed16b'), teamdatadf, pointcof, wincof, rankcof, ratiocof)
    except:
        pass
    try:
        data['d1r3seed11'] = whoWins(data.get('d1r3seed11a'), data.get('d1r3seed11b'), teamdatadf, pointcof, wincof, rankcof, ratiocof)
    except:
        pass
    try:
        data['d1r4seed16'] = whoWins(data.get('d1r4seed16a'), data.get('d1r4seed16b'), teamdatadf, pointcof, wincof, rankcof, ratiocof)
    except:
        pass
    try:
        data['d1r4seed11'] = whoWins(data.get('d1r4seed11a'), data.get('d1r4seed11b'), teamdatadf, pointcof, wincof, rankcof, ratiocof)
    except:
        pass
    try:
        data['d1r4seed12'] = whoWins(data.get('d1r4seed12a'), data.get('d1r4seed12b'), teamdatadf, pointcof, wincof, rankcof, ratiocof)
    except:
        pass

    # Simulates and stores each round until winner is determined
    champion = {}
    round1winners = roundResults(data, 1, teamdatadf, pointcof, wincof, rankcof, ratiocof)
    round2winners = roundResults(round1winners, 2, teamdatadf, pointcof, wincof, rankcof, ratiocof)
    round3winners = roundResults(round2winners, 3, teamdatadf, pointcof, wincof, rankcof, ratiocof)
    round4winners = roundResults(round3winners, 4, teamdatadf, pointcof, wincof, rankcof, ratiocof)
    round5winners = {'d6r1seed1': whoWins(round4winners.get('d5r1seed1'), round4winners.get('d5r4seed1'), teamdatadf, pointcof, wincof, rankcof, ratiocof),
                     'd6r1seed2': whoWins(round4winners.get('d5r2seed1'), round4winners.get('d5r3seed1'), teamdatadf, pointcof, wincof, rankcof, ratiocof)}
    champion['d7r1seed1'] = whoWins(round5winners.get('d6r1seed1'), round5winners.get('d6r1seed2'), teamdatadf, pointcof, wincof, rankcof, ratiocof)

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
    datafile = teamdatafile.replace('.csv', '')
    # with open(f'{simbracketpath}{datafile}-{pointcof}-{wincof}-{rankcof}-{ratiocof}-Sim.yaml', 'w') as f:
    #     yaml.dump(totalsimData, f, default_flow_style=False)
    with open(f'{simbracketpath}{datafile}-{pointcof}-{wincof}-{rankcof}-{ratiocof}-Sim.csv', 'w') as f:
        for key in totalsimData.keys():
            f.write("%s, %s\n" % (key, totalsimData[key]))

    return None


def populateBracket(simbracket):
    # Creates dataframe with simbracket
    df = pd.read_csv(f'{simbracketpath}{simbracket}')
    filename = simbracket.rstrip('.csv')
    #  Adds sheet with simbracket data
    with pd.ExcelWriter(f'{simbracketpath}Sim_Bracket.xlsx', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=filename)


    return None
