from utilities import bracketpath
import yaml
from AnalyzeGame import whoWins
from math import pow

with open(bracketpath + 'Bracket2021.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

    # First 4 games
    data['r1seed16'] = whoWins(data.get('r1seed16a'), data.get('r1seed16b'))
    data['r1seed12'] = whoWins(data.get('r1seed12a'), data.get('r1seed12b'))
    data['r4seed16'] = whoWins(data.get('r4seed16a'), data.get('r4seed16b'))
    data['r4seed12'] = whoWins(data.get('r4seed12a'), data.get('r4seed12b'))
    print(data.get('r1seed16'), data.get('r1seed12'), data.get('r4seed16'), data.get('r4seed12'))


def roundResults(teams, round):
    # Tests each game for defined round
    winners = {}

    # Loops through each game by region
    for x in range(1, 5):
        for y in range(1, int(pow(2, 4-round) + 1)):
            winners['r' + str(x) + 'seed' + str(y)] = whoWins(teams.get('r' + str(x) + 'seed' + str(y)), \
                                                              teams.get('r' + str(x) + 'seed' + str(int(pow(2, 5-round) + 1-y))))

    return winners


round1winners = roundResults(data, 1)
round2winners = roundResults(round1winners, 2)
round3winners = roundResults(round2winners, 3)
round4winners = roundResults(round3winners, 4)
round5winners = [whoWins(round4winners.get('r1seed1'), round4winners.get('r4seed1')), \
                 whoWins(round4winners.get('r2seed1'), round4winners.get('r3seed1'))]
champion = whoWins(round5winners[0], round5winners[1])

print(round1winners)
print(round2winners)
print(round3winners)
print(round4winners)
print(round5winners)
print(champion)
