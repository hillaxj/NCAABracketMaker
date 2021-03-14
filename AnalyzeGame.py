from utilities import datapath
import pandas as pd
import ast
import logging as log


def whoWins(team1, team2, teamdatadf):
    # Selects winner based on team records

    # Pulls each team's wins and losses from team data csv
    team1Ratio = teamdatadf.at[team1, 'Team Win Ratio']
    team2Ratio = teamdatadf.at[team2, 'Team Win Ratio']
    team1Schedule = teamdatadf.at[team1, 'Schedule Strength']
    team2Schedule = teamdatadf.at[team2, 'Schedule Strength']

    # Compares wins and losses, tie goes to team2
    if team1Ratio * team1Schedule >= team2Ratio * team2Schedule:
        winner = team1
    else:
        winner = team2

    return winner


def scheduleStrength(teamdatafile, winfactor, rankfactor, pointsfactor, schedulefactor):
    # Calculates value for schedule difficulty
    # Reads csv file
    df = pd.read_csv(datapath + teamdatafile, index_col='Team Name')
    teams = df.index.tolist()
    strlist = []

    for team in teams:
        # Creates dict of games played
        schedule = ast.literal_eval(df.at[team, 'Team Schedule Results'])
        opponentStrength = []
        # Iterates through games played and calculates strength
        for i in range(1, len(schedule) + 1):
            try:
                # Opponent win ratio from csv
                sched = schedule.get(i)
                opponentWinRatio = df.at[sched[1], 'Team Win Ratio']
                # Opponent rank factor
                if sched[2] != 'N/A':
                    opponentRank = (26-int(sched[2])) / 25
                else:
                    opponentRank = 0
                # Point differential factor, may need tweaks
                gamePoints = (100 - abs(int(sched[4]) - int(sched[5])))/100
                opponentStrength.append((winfactor * opponentWinRatio + rankfactor*opponentRank + \
                                         pointsfactor * gamePoints)/schedulefactor)

            except:
                continue

        strlist.append(sum(opponentStrength) / len(opponentStrength))
    df['Schedule Strength'] = strlist
    df.to_csv(datapath + teamdatafile)

    return None
