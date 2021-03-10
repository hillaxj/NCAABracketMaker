import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging as log
import re
from utilities import datapath

# common fxn parameters
headers = {"Accept-Language": "en-US, en;q=0.5"}


def getTeamList(gender, league, sport):
    # Adds each team ID from complete team list url to list and returns list
    # url for mens NCAA team list
    urlTeams = 'https://www.espn.com/' + gender + '-' + league + '-' + sport + '/teams'
    teamIDs = []

    results = requests.get(urlTeams, headers=headers)
    soup = BeautifulSoup(results.text, "html.parser")

    # Finds string containing team ID based on stats button
    id_div = soup.find_all('a', attrs={'href': re.compile("/team/schedule/_/id")})

    # Trims excess text from HTML to get only team ID, adds ID to list
    for team in id_div:
        team = str(team).replace('<a class="AnchorLink" href="/' + gender + '-' + league + '-' + sport + \
                                 '/team/schedule/_/id/', '')
        team = team.replace('" tabindex="0">Schedule</a>', '')
        teamIDs.append(team)

    return teamIDs


def getTeamData(gender, league, sport, year):
    # Generates CSV with all team names, mascots, and win/loss record

    # url for mens NCAA team schedule
    urlBase = 'https://www.espn.com/' + gender + '-' + league + '-' + sport + '/team/schedule/_/id/'

    # Initialize lists
    teamName = []
    teamMascot = []
    teamWinRecord = []
    teamLossRecord = []
    teamWinRatio = []
    teamIDList = []
    teamScheduleResults = []
    # Test mens teams list
    # teamIDs = [2473, 127, 251, 399, 171, 172]
    # Test women's teams list
    # teamIDs = [24, 12, 2463, 62, 300, 2483, 26]
    teamIDs = getTeamList(gender, league, sport)

    # Iterate through each teamID and populate list
    for id in teamIDs:
        # log.info('Team ' + str(id))
        urlTeam = urlBase + str(id) + '/season/' + year
        results = requests.get(urlTeam, headers=headers)
        soup = BeautifulSoup(results.text, "html.parser")
        # Find team info from HTML
        team_div = soup.find_all('div', class_='ClubhouseHeader__Main flex items-center pv3 justify-start')

        for container in team_div:

            try:
                # Find record and add win and loss records to teamWinRecord and teamLossRecord lists. Adds team ID to \
                # teamID list
                record = container.find('ul', class_='ClubhouseHeader__Record').find_all('li')
                record = record[0].text.split('-')
                # log.info(record[0] + ' ' + record[1])
                if record[0] == '0' and record[1] == '0':
                    continue
                else:
                    teamWinRecord.append(record[0])
                    teamLossRecord.append(record[1])
                    teamWinRatio.append(int(record[0]) / (int(record[0]) + int(record[1])))
                    teamIDList.append(id)
            except:
                continue

            # Find team name and add name to teamName list
            name = container.h1.find_all('span', class_='db')
            try:
                teamName.append(name[0].text)
            except:
                teamName.append('N/A')
            # Add mascot to teamMascot list
            try:
                teamMascot.append(name[1].text)
            except:
                teamMascot.append('N/A')
            # log.info(teamName[-1] + " " + teamMascot[-1])

        # Finds each row in schedule table
        schedule_div = soup.find_all('tr', attrs={'class': re.compile("Table__TR Table__TR--sm Table__even")})
        gameCount = 1
        teamSchedule = {}
        # Iterates through each row and extracts date, opponent, opponent rank, result, team score, and opponent score
        for container in schedule_div:
            # Finds data in each row
            try:
                lines = container.find_all('td')
                gameDate = lines[0].text

                # Removes excess info
                removedLoc = lines[1].text.split(' ')
                # Records team rank if present
                try:
                    int(removedLoc[1])
                    rankedTeam = True
                except:
                    rankedTeam = False

                if rankedTeam:
                    gameOpponent = ' '.join(removedLoc[2:]).strip().strip('*').strip()
                    gameOpponentRank = removedLoc[1]
                else:
                    gameOpponent = ' '.join(removedLoc[1:]).strip().strip('*').strip()
                    gameOpponentRank = 'N/A'

                # Extracts team result and add scores to correct var

                gameResult = lines[2].text[:1]
                gameScore = lines[2].text.replace('-', ' ')
                gameScore = gameScore.split(' ')
                if gameResult == 'W':
                    gameOpponentScore = gameScore[1]
                    gameTeamScore = gameScore[0][1:]
                elif gameResult == 'L':
                    gameTeamScore = gameScore[1]
                    gameOpponentScore = gameScore[0][1:]
                else:
                    continue
                teamSchedule[gameCount] = [gameDate, gameOpponent, gameOpponentRank, gameResult, gameTeamScore, \
                                              gameOpponentScore]
                gameCount = gameCount + 1
            except:
                continue

        if teamSchedule == {}:
            continue
        else:
            teamScheduleResults.append(teamSchedule)

    # Create dataframe for lists
    teamData = pd.DataFrame({
        'Team ID': teamIDList,
        'Team Name': teamName,
        'Team Mascot': teamMascot,
        'Team Win Record': teamWinRecord,
        'Team Loss Record': teamLossRecord,
        'Team Win Ratio': teamWinRatio,
        'Team Schedule Results': teamScheduleResults

    })

    # Export dataframe to CSV file in TeamData directory
    teamData.to_csv(datapath + gender + league + sport + year + '.csv')

    return None
