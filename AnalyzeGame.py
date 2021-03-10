from utilities import datapath
import pandas as pd


def whoWins(team1, team2, teamdatafile):
    # Selects winner based on team records

    # Pulls each team's wins and losses from team data csv
    df = pd.read_csv(datapath + teamdatafile, index_col='Team Name')
    team1Ratio = df.loc[team1, 'Team Win Record'] / (df.loc[team1, 'Team Loss Record'] + 1)
    team2Ratio = df.loc[team2, 'Team Win Record'] / (df.loc[team2, 'Team Loss Record'] + 1)

    # Compares wins and losses, tie goes to team2
    if team1Ratio >= team2Ratio:
        winner = team1
    else:
        winner = team2

    return winner
