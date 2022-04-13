from NCAABracketMaker.utilities import teampath
import pandas as pd
import ast


def whoWins(team1, team2, teamdatadf, pointcof, wincof, rankcof, ratiocof):
    """
    Selects winner based on team records
    :param team1: string, First team in game
    :param team2: string, Second team in game
    :param teamdatadf: dataframe, all team data
    :param pointcof:  float, points weight coefficient
    :param wincof: float, number of wins weight coefficient
    :param rankcof: float, top 25 team rank weight coefficient
    :param ratiocof: float, wins to losses weight coefficient
    :return: string, winning team
    """

    # Pulls each team's wins and losses from team data csv
    team1Ratio = teamdatadf.at[team1, 'Team Win Ratio']
    team2Ratio = teamdatadf.at[team2, 'Team Win Ratio']
    team1Points = teamdatadf.at[team1, 'Schedule Points']
    team2Points = teamdatadf.at[team2, 'Schedule Points']
    team1OppWins = teamdatadf.at[team1, 'Schedule Wins']
    team2OppWins = teamdatadf.at[team2, 'Schedule Wins']
    team1OppRank = teamdatadf.at[team1, 'Schedule Rank']
    team2OppRank = teamdatadf.at[team2, 'Schedule Rank']

    # Compares data from each team to determine winner, tie goes to team1
    if team1Ratio * ratiocof + team1Points * pointcof + team1OppRank * rankcof + team1OppWins * wincof >= \
            team2Ratio * ratiocof + team2Points * pointcof + team2OppRank * rankcof + team2OppWins * wincof:
        winner = team1
    else:
        winner = team2

    return winner


def scheduleStrength(teamdatafile):
    """
    Calculates value for schedule difficulty
    :param teamdatafile: string, filepath for csv of all team data
    :return: None, adds schedule strength parameters (Schedule Points, Schedule Wins, Schedule Rank) to teamdatafile
    """
    # Reads csv file
    df = pd.read_csv(f'{teampath}{teamdatafile}', index_col='Team Name')
    teams = df.index.tolist()
    pointList = []
    rankList = []
    winList = []

    for team in teams:
        # Creates dict of games played
        schedule = ast.literal_eval(df.at[team, 'Team Schedule Results'])
        oppWinList = []
        oppRankList = []
        pointsList = []
        # Iterates through games played and calculates strength
        for i in range(1, len(schedule) + 1):

            try:
                # Opponent win ratio from csv
                sched = schedule.get(i)
                oppWinList.append(df.at[sched[1], 'Team Win Ratio'])
                # Opponent rank factor
                if sched[2] != 'N/A':
                    oppRankList.append((26-int(sched[2])) / 25)
                else:
                    oppRankList.append(0)
                # Point differential factor, may need tweaks
                pointsList.append((100 - abs(int(sched[4]) - int(sched[5])))/100)

            except (LookupError, ValueError):
                continue

        pointList.append(sum(pointsList) / len(pointsList))
        rankList.append(sum(oppRankList) / len(oppRankList))
        winList.append(sum(oppWinList) / len(oppWinList))

    df['Schedule Points'] = pointList
    df['Schedule Wins'] = winList
    df['Schedule Rank'] = rankList
    # drop .csv at end of teamdatafile
    teamdatafile = teamdatafile.replace('.csv', '')
    df.to_csv(f'{teampath}{teamdatafile}.csv')

    return None
