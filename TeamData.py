import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
headers = {"Accept-Language": "en-US, en;q=0.5"}
urlBase = "https://www.espn.com/mens-college-basketball/team/schedule/_/id/"

teamName = []
teamMasc = []
teamRecord = []
teamID = 2752


# while teamID < 3000:
urlTeam = urlBase + str(teamID)
results = requests.get(urlTeam, headers=headers)
soup = BeautifulSoup(results.text, "html.parser")
team_div = soup.find_all('div', class_='ClubhouseHeader__Main flex items-center pv3 justify-start')

print(team_div)
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