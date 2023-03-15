import requests
from bs4 import BeautifulSoup

import pandas as pd

def getPlayerValue(url):
    headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    page = url
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    Players = pageSoup.findAll("img", {"class": "bilderrahmen-fixed lazy lazy"})
    Age = pageSoup.findAll("td", {"class": "zentriert"})
    Values = pageSoup.findAll("td", {"class": "rechts hauptlink"})
    Nation = pageSoup.findAll("h1", {"class":"data-header__headline-wrapper data-header__headline-wrapper--oswald"})
    PlayersList = []
    AgeList = []
    ValuesList = []
    NationalityList = []
    # get the names
    for i in range(0, len(Players)):
        PlayersList.append(str(Players[i]).split('" class', 1)[0].split('<img alt="', 1)[1])
    # get the values
    for i in range(0, len(Values)):
        ValuesList.append(Values[i].text)
    # get the nationality
    for i in range(0, len(Players)):
        NationalityList.append((str(Nation).split('</h1>', 1)[0].split('[<h1 class="data-header__headline-wrapper data-header__headline-wrapper--oswald">',1)[1]).strip())

    cleanedValues = []
    for a in list(range(len(ValuesList))):
        if 'm' in ValuesList[a]:
            x = ValuesList[a]
            cleanedValues.append(float(str(ValuesList[a]).split("m")[0].split('€')[1]) * 1000000)
        elif 'k' in ValuesList[a]:
            x = ValuesList[a]
            cleanedValues.append(float(str(ValuesList[a]).split("k")[0].split('€')[1]) * 1000)
        else:
            cleanedValues.append(0)


    return PlayersList, cleanedValues, NationalityList

def transfermarketValue(competition):
    if "EM" in competition:
        url = "https://www.transfermarkt.com/europameisterschaft-2020/teilnehmer/pokalwettbewerb/EM20/saison_id/2020"
        season = "?saison_id=2020"
        numberOfCompetitors = 24
    else:
        url = "https://www.transfermarkt.com/weltmeisterschaft-2022/teilnehmer/pokalwettbewerb/WM22/saison_id/2021"
        season = "?saison_id=2021"
        numberOfCompetitors = 32

    # get all countries back
    headers = {'User-Agent':
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    pageTree = requests.get(url, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    url_country = pageSoup.findAll("td", {"class":"zentriert no-border-rechts"})
    url_countries = []
    # get all the urls of all countries that participated in the wc 2022 (on transfermarkt this is scripted as season 2021)
    for i in range(0, numberOfCompetitors):
        url_countries.append("https://www.transfermarkt.com"+str(url_country[i]).split('" title', 1)[0].split('<a href="',1)[1]+season)


    #go through all countries and add their squad to the players that participated at the world cup
    PlayersList = []
    PlayerValues = []
    PlayersNation = []
    counter = 0
    for team in url_countries:
        print(counter, " / ", len(url_countries))
        players, values, nationality = getPlayerValue(team)
        PlayersList = PlayersList + players
        PlayerValues = PlayerValues + values
        PlayersNation = PlayersNation + nationality
        counter += 1

    df = pd.DataFrame({"player": PlayersList,
                               "value": PlayerValues,
                          "nationality": PlayersNation})
    return df

