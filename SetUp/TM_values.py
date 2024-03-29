import re
from difflib import SequenceMatcher
from typing import List
from scipy.stats import ttest_ind
import requests
from bs4 import BeautifulSoup

import pandas as pd


def tTestMarketValue(df):
    q = pd.DataFrame()
    q['quantile'] = df['value'].quantile([0.25, 0.5, 0.75])
    q.reset_index(drop=True, inplace=True)
    median = df['value'].median()
    mean = df['value'].mean()

    # create empty lists, that can be filled later

    value_separation: List[int] = [0] * len(q['quantile'])
    t_stat: List[float] = [0.0] * len(q['quantile'])
    p_values: List[float] = [0.0] * len(q['quantile'])
    len_df_valuable: List[int] = [0] * len(q['quantile'])
    len_df_in_cheaper: List[int] = [0] * len(q['quantile'])

    for quant in range(len(q)):
        # separate the dataframe according to the current shot separation
        dfValuable = df.loc[df['value'] >= q['quantile'][quant]]
        dfCheaper = df.loc[df['value'] < q['quantile'][quant]]

        # could be that it is empty, since no shots from the leading team were taken
        # therefore try as error handling
        shotValuesOne = dfValuable['xG_Delta_decision_alternative'].values.tolist()
        shotValuesTwo = dfCheaper['xG_Delta_decision_alternative'].values.tolist()

        t_stat[quant], p_values[quant] = ttest_ind(shotValuesOne, shotValuesTwo)
        value_separation[quant] = q['quantile'][quant]
        len_df_valuable[quant] = len(dfValuable['xG_Delta_decision_alternative'])
        len_df_in_cheaper[quant] = len(dfCheaper['xG_Delta_decision_alternative'])

    dataMarketValue = {'value_separation': value_separation,
                       'T-stat': t_stat,
                       'P-Val': p_values,
                       'number_shots_valuable': len_df_valuable,
                       'number_shots_cheaper': len_df_in_cheaper}
    return dataMarketValue
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

def transfermarketValue(dfCompetition, competition):
    url = ""
    season = ""
    numberOfCompetitors = 0
    if "EM20" in competition:
        url = "https://www.transfermarkt.com/europameisterschaft-2020/teilnehmer/pokalwettbewerb/EM20/saison_id/2020"
        season = "?saison_id=2020"
        numberOfCompetitors = 24
    elif "WM22" in competition:
        url = "https://www.transfermarkt.com/weltmeisterschaft-2022/teilnehmer/pokalwettbewerb/WM22/saison_id/2021"
        season = "?saison_id=2021"
        numberOfCompetitors = 32
    elif "EM16" in competition:
        url = "https://www.transfermarkt.com/europameisterschaft-2016/teilnehmer/pokalwettbewerb/EM16/saison_id/2015"
        season = "?saison_id=2021"
        numberOfCompetitors = 24
    elif "WM18" in competition:
        url = "https://www.transfermarkt.com/weltmeisterschaft-2018/teilnehmer/pokalwettbewerb/WM18/saison_id/2017"
        season = "?saison_id=2017"
        numberOfCompetitors = 32

    # get all countries back that participated in this championship
    headers = {'User-Agent':
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    pageTree = requests.get(url, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    url_country = pageSoup.findAll("td", {"class":"zentriert no-border-rechts"})
    url_countries = []
    # get all the urls of all countries that participated in the competition looked for (the season number is always one below of the competition year)
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

    dfValues = pd.DataFrame({"player": PlayersList,
                               "value": PlayerValues,
                          "nationality": PlayersNation})

    dfCompetition, added_attributes = join(dfCompetition=dfCompetition, dfValues=dfValues)
    return dfCompetition

def exceptionCases(player_name, dfValues):
    name_searched = None
    if player_name == "Carlos Henrique Casimiro":
        name_searched = "Casemiro"
    elif player_name == "Raphael Dias Belloli":
        name_searched = "Raphinha"
    elif player_name == "Lucas Tolentino Coelho de Lima":
        name_searched = "Lucas Paquetá"
    elif player_name == "Saud Abdullah Abdul Hamid":
        name_searched = "Saud Abdulhamid"
    elif player_name == "Vitor Machado Ferreira":
        name_searched = "Vitinha"
    elif player_name == "İbrahim Halil Dervişoğlu":
        name_searched = "Halil Dervisoglu"
    elif player_name == "Tomáš Holeš":
        name_searched = "Tomas Holes"
    elif player_name == "Jorge Resurrección Merodio":
        name_searched = "Koke"
    elif player_name == "Mehmet Zeki Çelik":
        name_searched = "Zeki Celik"
    elif player_name == "Fahad Mosaed Al Muwallad Al Harbi":
        name_searched = "Fahad Al-Muwallad"
    elif player_name == "Fernando Luiz Rosa":
        name_searched = "Fernandinho"
    elif player_name == "Ghilane Chalali":
        name_searched = "Ghaylen Chaaleli"
    elif player_name == "Papa Alioune N''Diaye":
        name_searched = "Badou Ndiaye"
    elif player_name == "Mohanad Aseri Abu Radiah":
        name_searched = "Muhannad Assiri"
    elif player_name == "Oghenekaro Etebo":
        name_searched = "Peter Etebo"
    try:
        value = dfValues['value'][dfValues['player'] == name_searched]
        value.reset_index(drop=True, inplace=True)
        value = value[0]
    except KeyError:
        value = None
    return value
def join(dfCompetition, dfValues):
    values = []
    # go through every player in the competition
    for row in range(len(dfCompetition)):

        value = None
        # and check if there is a player with the same name in the value list
        # this has to be done with a regex, since transfermarkt can save players with different spellings
        for player in range(len(dfValues)):
            # deb
            x = dfValues['player'][player]
            y =  dfCompetition['player'][row]
            # if the player has not the same nationality, we don't have to calculate too much and can save time
            # skip then to the next player
            if dfValues['nationality'][player].casefold() != dfCompetition['team'][row].casefold():
                continue
            # player with similar name or same name has be found add his value
            # it is guaranteed that the players have the same nationality.
            # so here it could only generate a mix-up if two player of the same nationality have the same name
            # similar, because it is checked with keyword 'in'
            # example:
            # dfValues Player = Max Mustermann | dfCompetition Player = Max Mustermann Peter
            # this would give us true since Max Mustermann is in Max Mustermann Peter
            # this only works if the additional names are in the end
            # break statement is used, because when we found the matching player we dont want to continue searching
            elif dfValues['player'][player].casefold() in dfCompetition['player'][row].casefold():
                value = dfValues['value'][player]
                break
            # but if the 3rd and 4th names are in the middle we have to use a trick
            # Example: Max Mustermann vs. Max Peter Mustermann, keyword 'in' gives false
            # if the name consists out of more than 3 words, than only keep the first and last name
            elif len(re.findall(r'\w+', dfCompetition['player'][row])) >= 3:
                name_of_player = dfCompetition['player'][row].split()
                name_of_player = name_of_player[0] + " " + name_of_player[-1]
                # when the middle names are thrown away, check again Max Mustermann is in Max (Peter) Mustermann
                if dfValues['player'][player] in name_of_player:
                    value = dfValues['value'][player]
                    break
                    # if the name is still not found in the database and the name consists out of three or more names,
                    # it is searched for a name with +75% similiarity and the same nationality
                elif SequenceMatcher(a=name_of_player, b=dfValues['player'][player]).ratio() >= 0.75:
                    value = dfValues['value'][player]
                    break
                # if the player is still not found, then we only check if the last name of our player is in the name of the shooting player
                # of course the nation has to be the same
                # this is not optimal if the player has a name which cannot be compared and multiple players in the team have the same last name
                # it is not guaranteed that we take the correct last name, we always take the last one with this implementation
                elif dfValues['player'][player].split()[-1] in dfCompetition['player'][row]:
                    value = dfValues['value'][player]


            # if one has only two names but a lot of different special characters, his name should be compared
            # if the names match with over 75% the name is taken
            # Example: Hakan Calhanoglu | Hakan Çalhanoğlu would match this case
            elif SequenceMatcher(a=dfCompetition['player'][row], b=dfValues['player'][player]).ratio() >= 0.75:
                value = dfValues['value'][player]
                break
        # if we still couldn't find a player, we can add the value manually with an exception case
        if value is None:
            value = exceptionCases(dfCompetition['player'][row], dfValues)
        if value is None:
            print(dfCompetition['player'][row])
        # if a player has been found that is similar to the original player, then we add a value to it,
        # otherwise a None entry is created
        values.append(value)

    dfCompetition['value'] = values
    return dfCompetition, 'value'
