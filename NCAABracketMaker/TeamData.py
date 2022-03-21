import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging as log
import re
from NCAABracketMaker.utilities import teampath, bracketpath
from NCAABracketMaker.AnalyzeGame import scheduleStrength

# common fxn parameters
headers = {"Accept-Language": "en-US, en;q=0.5"}


def getTeamList(sex):
    """
    Generates a list of all the teams in the league
    :param sex: str, mens or womens league
    :return: list, list of strings with all team names
    """
    # Adds each team ID from complete team list url to list and returns list
    # url for mens NCAA team list
    # Alternate data source 'https://basketball.realgm.com/ncaa/teams'
    urlTeams = 'https://www.espn.com/' + sex + '-college-basketball/teams'
    teamIDs = []

    results = requests.get(urlTeams, headers=headers)
    soup = BeautifulSoup(results.text, "html.parser")

    # Finds string containing team ID based on stats button
    id_div = soup.find_all('a', attrs={'href': re.compile("/team/schedule/_/id")})

    # Trims excess text from HTML to get only team ID, adds ID to list
    for team in id_div:
        team = str(team).replace('<a class="AnchorLink" href="/' + sex + '-college-basketball/team/schedule/_/id/', '')
        team = team.replace('" tabindex="0">Schedule</a>', '')
        teamIDs.append(team)

    teamIDs = list(dict.fromkeys(teamIDs))

    return teamIDs


def getTeamData(sex, year):
    """
    Generates CSV with all team names, mascots, and win/loss record
    :param sex: str, mens or womens league
    :param year: int, year of data being retrieved
    :return: None, creates csv of team data for each team
    """

    # url for mens NCAA team schedule
    # Alternate data source 'https://basketball.realgm.com/ncaa/team-stats', \
    # 'https://basketball.realgm.com/ncaa/conferences/West-Coast-Conference/11/Gonzaga/332/Schedule'
    urlBase = 'https://www.espn.com/' + sex + '-college-basketball/team/schedule/_/id/'

    # Initialize lists
    teamName = []
    teamMascot = []
    teamWinRecord = []
    teamLossRecord = []
    teamWinRatio = []
    teamIDList = []
    teamScheduleResults = []
    teamIDs = getTeamList(sex)

    # Iterate through each teamID and populate list
    for id in teamIDs:
        log.info('Year ' + str(year) + ' : ' + 'Team ' + str(id))
        urlTeam = urlBase + str(id) + '/season/' + str(year)
        with requests.get(urlTeam, headers=headers):
            results = requests.get(urlTeam, headers=headers)
            soup = BeautifulSoup(results.text, "html.parser")

        # Finds each row in schedule table
        schedule_div = soup.find_all('tr', attrs={'class': re.compile("Table__TR Table__TR--sm Table__even")})
        gameCount = 1
        teamSchedule = {}
        winRecord = 0
        loseRecord = 0

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
                    winRecord = winRecord + 1
                elif gameResult == 'L':
                    gameTeamScore = gameScore[1]
                    gameOpponentScore = gameScore[0][1:]
                    loseRecord = loseRecord + 1
                else:
                    continue
                teamSchedule[gameCount] = [gameDate, gameOpponent, gameOpponentRank, gameResult, gameTeamScore,
                                              gameOpponentScore]
                gameCount = gameCount + 1
            except:
                continue

        if teamSchedule == {}:
            continue
        else:
            # Find team info from HTML
            team_div = soup.find_all('div', class_='ClubhouseHeader__Main flex items-center pv3 justify-start')

            for container in team_div:

                # Find team name and add name to teamName list
                name = container.h1.find_all('span', class_='db')
                teamName.append(name[0].text)

                # Add mascot to teamMascot list
                try:
                    teamMascot.append(name[1].text)
                except:
                    teamMascot.append('N/A')
            teamWinRecord.append(winRecord)
            teamLossRecord.append(loseRecord)
            teamWinRatio.append(winRecord / (winRecord + loseRecord))
            teamScheduleResults.append(teamSchedule)
            teamIDList.append(id)

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
    teamData.to_csv(teampath + sex + str(year) + '.csv')
    scheduleStrength(f'{sex}{year}.csv')

    return None


def populateResults(year):
    """
    Populates results for past brackets
    :param year: int, year for past results
    :return: None, creates csv file with past results
    """
    # All NCAA mens data 2019-1985
    # urlBracket = 'https://query.data.world/s/esvsa75otwudjalobphshkfrcn72dr'
    if year == 2020:
        # No 2020 bracket exists
        with open(bracketpath + str(year) + 'results.csv', 'w') as f:
            f.write('Coronavirus')
        print('2020 Coronavirus')
        return None
    else:
        print(year)

    csv = pd.read_csv(bracketpath + 'Big_Dance_CSV.csv', index_col=0)

    teams = {}
    # Loops through each row in pd
    for row in csv.itertuples():
        # Records row data
        if row[0] == year:
            team = {}
            for i in range(6, 8):
                # Corrects team names from csv
                try:
                    team[i] = nameCheck(row[i])
                except:
                    pass

            teams['d' + str(row[1]) + 'r' + str(row[2]) + 'seed' + str(row[4])] = team[6]
            # Checks for duplicate seeds
            try:
                if len(teams['d' + str(row[1]) + 'r' + str(row[2]) + 'seed' + str(row[9])]) > 0:
                    teams['d' + str(row[1]) + 'r' + str(row[2]) + 'seed' + str(row[9]+row[8])] = team[7]
            except:
                teams['d' + str(row[1]) + 'r' + str(row[2]) + 'seed' + str(row[9])] = team[7]
            # Determines champion
            if row[1] == 6:
                if row[5] > row[8]:
                    teams['d' + str(row[1] + 1) + 'r' + str(row[2]) + 'seed' + str(row[4])] = team[6]
                else:
                    teams['d' + str(row[1] + 1) + 'r' + str(row[2]) + 'seed' + str(row[4])] = team[7]

    # Dump teams dict into csv
    with open(bracketpath + str(year) + 'results.csv', 'w') as f:
        for key in teams.keys():
            f.write("%s, %s\n" % (key, teams[key]))

    return None


def nameCheck(teamName):
    """
    Checks names to ensure consistent naming
    :param teamName: str, team name to be checked
    :return: str, corrected team name
    """
    switch = {
        'Central Florida': 'UCF',
        'Gardner Webb': 'Gardner-Webb',
        'Wisconsin Milwaukee': 'Milwaukee',
        'Connecticut': 'UConn',
        'Illinois Chicago': 'UIC',
        'Texas San Antonio': 'UTSA',
        'Louisiana Lafayette': 'Louisiana',
        'Southeastern Louisiana': 'SE Louisiana',
        'Texas A&M Corpus Christi': 'Texas A&M-CC',
        'Miami Ohio': 'Miami (OH)',
        'Central Connecticut St': 'Central Connecticut',
        'Mount St Marys': 'Mount St. Mary\'s',
        'Cal St Fullerton': 'CSU Fullerton',
        'Texas Arlington': 'UT Arlington',
        'Cal St Northridge': 'CSU Northridge',
        'Morgan St': 'Morgan St',
        'Stephen F Austin': 'Stephen F. Austin',
        'Santa Barbara': 'UC Santa Barbara',
        'Arkansas Pine Bluff': 'Arkansas-Pine Bluff',
        'Long Island Brooklyn': 'Long Island University',
        'St Johns': 'St. John\'s',
        'Loyola Maryland': 'Loyola (MD)',
        'Southern Mississippi': 'Southern Miss',
        'Detroit': 'Detroit Mercy',
        'American': 'American',
        'Massachusetts': 'UMass',
        'Cal Irvine': 'UC Irvine',
        'Hawaii': 'Hawai\'i',
        'Cal St Bakersfield': 'CSU Bakersfield',
        'Wisconsin Green Bay': 'Green Bay',
        'Middle Tennessee St': 'Middle Tennessee',
        'Arkansas Little Rock': 'Little Rock',
        'College of Charleston': 'Charleston'

    }
    team = switch.get(teamName, teamName)

    if team.split(' ')[0] == 'St':
        if team.split(' ')[1] == 'Peters' or team.split(' ')[1] == 'Josephs' \
                or team.split(' ')[1] == 'Louis' or team.split(' ')[1] == 'Marys':
            team = team.replace('St', 'Saint').replace('Peters', 'Peter\'s').replace('Josephs',
                                                                            'Joseph\'s').replace('Marys', 'Mary\'s')
        else:
            team = team.replace('St', 'St.')
    # Morgan State for womens team
    elif team.split(' ')[-1] == 'St' and team != 'Morgan St':
        team = teamName.replace('St', 'State')

    return team


def getemptybracket(sex):
    # TODO get this function working
    urlbracket = 'http://www.espn.com/mens-college-basketball/tournament/bracket'
    bracket_teams = []
    bracket_seeds = []
    year = 2022
    results = requests.get(urlbracket, headers=headers)
    soup = BeautifulSoup(results.text, "html.parser")

    # Finds string containing team ID based on stats button
    id_div = soup.find_all('a', attrs={'href': re.compile("/team/_/id")})
    # Need to split by region then the following code

    # Finds string containing team seed and team ID
    seed_div = soup.find_all('b')
    # Trims excess text from HTML to get only team ID and seed, adds them to lists
    for seed in seed_div:
        team_seed = str(seed).rsplit('/')
        bracket_seeds.append(team_seed[0].replace('<b>', '').replace(' <a href="http:', ''))
        bracket_teams.append(team_seed[7])
    # for team in id_div:
    #     team = str(team).rsplit('/')
    #     bracket_teams.append(team[7])


    bracket_teams = list(dict.fromkeys(bracket_teams))

    csv = pd.read_csv(bracketpath + 'Big_Dance_CSV.csv', index_col=0)

    teams = {}
    # Loops through each row in pd
    for row in csv.itertuples():
        # Records row data
        if row[0] == year:
            team = {}
            for i in range(6, 8):
                # Corrects team names from csv
                try:
                    team[i] = nameCheck(row[i])
                except ValueError:
                    pass

            teams['d' + str(row[1]) + 'r' + str(row[2]) + 'seed' + str(row[4])] = team[6]
            # Checks for duplicate seeds
            try:
                if len(teams['d' + str(row[1]) + 'r' + str(row[2]) + 'seed' + str(row[9])]) > 0:
                    teams['d' + str(row[1]) + 'r' + str(row[2]) + 'seed' + str(row[9]+row[8])] = team[7]
            except ValueError:
                teams['d' + str(row[1]) + 'r' + str(row[2]) + 'seed' + str(row[9])] = team[7]
            # Determines champion
            if row[1] == 6:
                if row[5] > row[8]:
                    teams['d' + str(row[1] + 1) + 'r' + str(row[2]) + 'seed' + str(row[4])] = team[6]
                else:
                    teams['d' + str(row[1] + 1) + 'r' + str(row[2]) + 'seed' + str(row[4])] = team[7]

    # Dump teams dict into csv
    with open(bracketpath + str(year) + 'results.csv', 'w') as f:
        for key in teams.keys():
            f.write("%s, %s\n" % (key, teams[key]))

    return None
