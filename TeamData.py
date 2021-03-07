import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import logging as log
from utilities import datapath

# todo: List of team IDs from https://www.espn.com/mens-college-basketball/teams, \
#  iterate through list insted of all possible teams
# todo: import schedule data

def getTeamData():
    headers = {"Accept-Language": "en-US, en;q=0.5"}
    urlBase = "https://www.espn.com/mens-college-basketball/team/schedule/_/id/"

    teamName = []
    teamMascot = []
    teamRecord = []

    for teamID in range(1, 1000):
        log.info('Team ' + str(teamID))
        urlTeam = urlBase + str(teamID)
        results = requests.get(urlTeam, headers=headers)
        soup = BeautifulSoup(results.text, "html.parser")
        team_div = soup.find_all('div', class_='ClubhouseHeader__Main flex items-center pv3 justify-start')

        for container in team_div:

            try:
            # Record
                record = container.find('ul', class_='ClubhouseHeader__Record').find_all('li')
                log.info(record[0].text)
                teamRecord.append(record[0].text)
            except:
                continue

            # Name and Mascot
            name = container.h1.find_all('span', class_='db')
            log.info(name[0].text + ' ' + name[1].text)
            if name[0].text is not None:
                teamName.append(name[0].text)
            else:
                teamName.append('N/A')

            if name[1] is not None:
                teamMascot.append(name[1].text)
            else:
                teamMascot.append('N/A')



    teamData = pd.DataFrame({
        'Team Name': teamName,
        'Team Mascot': teamMascot,
        'Team Record': teamRecord

    })

    teamData.to_csv(datapath + "TeamData.csv")
        # print(teamName, teamMascot, teamRecord)
        # for container in movie_div:
        #     # Name
        #     name = container.h3.a.text
        #     titles.append(name)
        #     # Rank
        #     rank = container.h3.find('span', class_='lister-item-index').text
        #     ranks.append(rank)
        #     # year
        #     year = container.h3.find('span', class_='lister-item-year').text
        #     years.append(year)
        #     # Runtime
        #     time = container.find('span', class_='runtime').text if container.p.find('span', class_='runtime') else '-'
        #     times.append(time)
        #     # imdb Rating
        #     imdb = float(container.strong.text)
        #     imdb_ratings.append(imdb)
        #     # Metascore
        #     m_score = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else '-'
        #     metascores.append(m_score)
        #     # filter nv for votes
        #     nv = container.find_all('span', attrs={'name': 'nv'})
        #     vote = nv[0].text
        #     votes.append(vote)
        #     # filter nv for gross
        #     grosses = nv[1].text if len(nv) > 1 else '-'
        #     us_gross.append(grosses)
    return None

getTeamData()