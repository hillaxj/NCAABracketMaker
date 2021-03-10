from utilities import datapath
import pandas as pd
import ast


def whoWins(team1, team2, teamdatafile):
    # Selects winner based on team records

    # Pulls each team's wins and losses from team data csv
    df = pd.read_csv(datapath + teamdatafile, index_col='Team Name')
    team1Ratio = df.at[team1, 'Team Win Ratio']
    team2Ratio = df.at[team2, 'Team Win Ratio']

    # Compares wins and losses, tie goes to team2
    if team1Ratio >= team2Ratio:
        winner = team1
    else:
        winner = team2

    return winner


def scheduleStrength(teamdatafile):
    # Calculates value for schedule difficulty, need to tweak a lot
    # Reads csv file
    df = pd.read_csv(datapath + teamdatafile, index_col='Team Name')
    teams = df.index.tolist()
    strength = 1
    opponentStrength = []
    strlist = []

    for team in teams:
        # Creates dict of games played
        schedule = ast.literal_eval(df.at[team, 'Team Schedule Results'])
        # Iterates through games played and calculates strength based on opponent record
        for i in range(1, len(schedule) + 1):
            try:
                opponentStrength.append(df.at[schedule.get(i)[1], 'Team Win Ratio'])
                strength = sum(opponentStrength) / len(opponentStrength)
            except:
                continue
        strlist.append(strength)
    df['Schedule Strength'] = strlist
    df.to_csv(datapath + teamdatafile)

    return None
