# import all shots EM2020
from typing import List
import re
from SetUp import JSONtoDF, CONSTANTS
import pandas as pd
import ws_tm_values
from scipy.stats import ttest_ind
import ws_tm_values
from difflib import SequenceMatcher

#dfWMValues = ws_tm_values.transfermarketValue("WM")
#dfWMValues.to_json("ValuesWM.json")
dfWMValues = JSONtoDF.createDF("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Hypothesis_market_value/ValuesWM.json")

# dfEMValues = ws_tm_values.transfermarketValue("EM")

dfEM20 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONEM2020)
dfWM22 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONWM2022)
# since the statsbomb names contains 3rd ant 4th names and transfermarkt names does not contain these names,
# the join operator has to be built manually
values = []

for row in range(len(dfWM22)):
    found = False
    value = None
    if dfWM22['player'][row] == "Kang-In Lee":
        print("deb")
    for player in range(len(dfWMValues)):
        x = dfWMValues['player'][player]
        # if the player has not the same nationality, we don't have to calculate too much and cans save time
        # skip then to the next player
        if dfWMValues['nationality'][player].casefold() != dfWM22['team'][row].casefold():
            continue
        # player with similar name has be found add his value
        # this only works if the additional names are in the end
        # break statement is used, because when we found the matching player we dont want to continue searching
        elif dfWMValues['player'][player] in dfWM22['player'][row]:
            value = dfWMValues['value'][player]
            break
        # but if the 3rd and 4th names are in the middle we have to use a trick
        # if the name consists out of more than 3 words, than only keep the first and last name
        elif len(re.findall(r'\w+', dfWM22['player'][row])) >= 3:
            name_of_player = dfWM22['player'][row].split()
            name_of_player = name_of_player[0] +" "+ name_of_player[-1]
            if dfWMValues['player'][player] in name_of_player:
                value = dfWMValues['value'][player]
                break
                # if the name is still not found in the database, but a name with +75% similiarity is found and the nationality is the same, the name is taken
            elif SequenceMatcher(a=name_of_player, b=dfWMValues['player'][player]).ratio() >= 0.75:
                value = dfWMValues['value'][player]
                break
            # if the player is still not found, then we only check if the last name of our player is in the name of the shooting player
            # of course the nation has to be the same
            # this is not optimal if the player has a name which cannot be compared and multiple players in the team have the same last name
            # it is not guaranteed that we take the correct last name, we always take the last one with this implementation
            elif dfWMValues['player'][player].split()[-1] in dfWM22['player'][row]:
                value = dfWMValues['value'][player]


        #if one has only two names but a lot of different special characters, his name should be compared
        elif SequenceMatcher(a=dfWM22['player'][row] , b=dfWMValues['player'][player]).ratio() >= 0.75:
            value = dfWMValues['value'][player]
            break




    # if a player has been found that is similar to the original player, then we add a value to it,
    # otherwise a None entry is created
    values.append(value)




dfWM22['value'] = values
dfWM22 = dfWM22[["player", "value", "team"]]
