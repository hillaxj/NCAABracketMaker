from utilities import bracketpath
import yaml
from AnalyzeGame import whoWins
from math import pow
import PyPDF2


def roundResults(teams, round, teamdatafile):
    # Tests each game for defined round
    winners = {}

    # Loops through each game by region

    for x in range(1, 5):
        for y in range(1, int(pow(2, 4-round) + 1)):
            winners['d' + str(round+1) + 'r' + str(x) + 'seed' + str(y)] = whoWins(teams.get('d' + str(round) + 'r' + str(x) + 'seed' + str(y)), \
                                                              teams.get('d' + str(round) + 'r' + str(x) + 'seed' + str(int(pow(2, 5-round) \
                                                                                                + 1-y))), teamdatafile)

    return winners


def bracketSim(bracketfile, teamdatafile):

    # Simulates all games in the supplied brackets based on teamdatafile info
    with open(bracketpath + bracketfile) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    # First 4 games
    try:
        data['d1r1seed16'] = whoWins(data.get('d1r1seed16a'), data.get('d1r1seed16b'), teamdatafile)
        data['d1r1seed12'] = whoWins(data.get('d1r1seed12a'), data.get('d1r1seed12b'), teamdatafile)
        data['d1r4seed16'] = whoWins(data.get('d1r4seed16a'), data.get('d1r4seed16b'), teamdatafile)
        data['d1r4seed12'] = whoWins(data.get('d1r4seed12a'), data.get('d1r4seed12b'), teamdatafile)
        print(data.get('d1r1seed16'), data.get('d1r1seed12'), data.get('d1r4seed16'), data.get('d1r4seed12'))
    except:
        pass

    # Simulates and stores each round until winner is determined
    champion = {}
    round1winners = roundResults(data, 1, teamdatafile)
    round2winners = roundResults(round1winners, 2, teamdatafile)
    round3winners = roundResults(round2winners, 3, teamdatafile)
    round4winners = roundResults(round3winners, 4, teamdatafile)
    round5winners = {'d6r1seed1': whoWins(round4winners.get('d5r1seed1'), round4winners.get('d5r4seed1'), teamdatafile), \
                     'd6r1seed2': whoWins(round4winners.get('d5r2seed1'), round4winners.get('d5r3seed1'), teamdatafile)}
    champion['d7r1seed1'] = whoWins(round5winners.get('d6r1seed1'), round5winners.get('d6r1seed2'), teamdatafile)

    print(round1winners)
    print(round2winners)
    print(round3winners)
    print(round4winners)
    print(round5winners)
    print(champion)

    totalsimData = {**data, **round1winners, **round2winners, **round3winners, **round4winners, **round5winners, **champion}

    with open(bracketpath + teamdatafile.replace('.csv', '') + 'SimResults.yaml', 'w') as f:
        yaml.dump(totalsimData, f, default_flow_style=False)

    return None


def popBracket():

    pdf = open(bracketpath + 'NCAA Bracket clean.pdf')
    readpdf = PyPDF2.PdfFileReader(pdf)



    return None
