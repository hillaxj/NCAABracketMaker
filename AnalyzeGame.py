from utilities import datapath
import pandas as pd


def whoWins(team1, team2, teamdatafile):
    # Selects winner based on team records

    # Pulls each team's wins and losses from TeamData.csv
    df = pd.read_csv(datapath + teamdatafile, index_col='Team Name')
    team1wins = df.loc[team1, 'Team Win Record']
    team1losses = df.loc[team1, 'Team Loss Record']
    team2wins = df.loc[team2, 'Team Win Record']
    team2losses = df.loc[team2, 'Team Loss Record']

    # Compares wins and losses, tie goes to team2
    if team1wins < team2wins and team1losses > team2losses:
        winner = team2
    else:
        winner = team1

    return winner
