from utilities import bracketpath
import yaml
from AnalyzeGame import whoWins
from math import pow
from fpdf import FPDF


def roundResults(teams, round, teamdatafile):
    # Tests each game for defined round
    winners = {}

    # Loops through each game by region
    for x in range(1, 5):
        for y in range(1, int(pow(2, 4-round) + 1)):
            winners['r' + str(x) + 'seed' + str(y)] = whoWins(teams.get('r' + str(x) + 'seed' + str(y)), \
                                                              teams.get('r' + str(x) + 'seed' + str(int(pow(2, 5-round) + 1-y))), teamdatafile)

    return winners


def bracketSim(bracketfile, teamdatafile):

    # Simulates all games in the supplied brackets based on teamdatafile info
    with open(bracketpath + bracketfile) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    # First 4 games
    try:
        data['r1seed16'] = whoWins(data.get('r1seed16a'), data.get('r1seed16b'), teamdatafile)
        data['r1seed12'] = whoWins(data.get('r1seed12a'), data.get('r1seed12b'), teamdatafile)
        data['r4seed16'] = whoWins(data.get('r4seed16a'), data.get('r4seed16b'), teamdatafile)
        data['r4seed12'] = whoWins(data.get('r4seed12a'), data.get('r4seed12b'), teamdatafile)
        print(data.get('r1seed16'), data.get('r1seed12'), data.get('r4seed16'), data.get('r4seed12'))
    except:
        pass

    # Simulates and stores each round until winner is determined
    round1winners = roundResults(data, 1, teamdatafile)
    round2winners = roundResults(round1winners, 2, teamdatafile)
    round3winners = roundResults(round2winners, 3, teamdatafile)
    round4winners = roundResults(round3winners, 4, teamdatafile)
    round5winners = [whoWins(round4winners.get('r1seed1'), round4winners.get('r4seed1'), teamdatafile), \
                     whoWins(round4winners.get('r2seed1'), round4winners.get('r3seed1'), teamdatafile)]
    champion = whoWins(round5winners[0], round5winners[1], teamdatafile)

    print(round1winners)
    print(round2winners)
    print(round3winners)
    print(round4winners)
    print(round5winners)
    print(champion)

    return None


def popBracket():
    pdf_h = 210
    pdf_w = 297

    class PDF(FPDF):
        def lines(self):
            self.set_line_width(0.0)
            self.line(5.0, 5.0, 205.0, 5.0)  # top one
            self.line(5.0, 202.0, 205.0, 202.0)  # bottom one
            self.line(5.0, 5.0, 5.0, 202.0)  # left one
            self.line(205.0, 5.0, 205.0, 202.0)


    lineheight = pdf_h / 32
    linelength = pdf_w / 12

    pdf = PDF(orientation='L')

    # pdf.add_page()
    pdf.output('test.pdf')

    return None
