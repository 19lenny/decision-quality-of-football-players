from statsbombpy import sb
import pandas as pd
from SetUp import DataManipulationAngleDistance

# 55,43 is the code of the EM 2020. This can be found in the excel overview "CompetitionOverview.xlsx"
# 43,106 is the code of the WM 2022. This can be found in the excel overview "CompetitionOverview.xlsx"
dfMatchesEM2020 = pd.DataFrame(sb.matches(55, 43))
dfMatchesWM2022 = pd.DataFrame(sb.matches(43, 106))

# all matchID's EM2020
matchIdEM2020 = dfMatchesEM2020.match_id.values.tolist()
# all matchID's WM2022
matchIdWM2022 = dfMatchesWM2022.match_id.values.tolist()

# initialize df
dfEventsEM2020 = pd.DataFrame()
dfEventsWM2022 = pd.DataFrame()

# get every event from every game from the matches of em2020, and wm 2022
# save these events
for event in matchIdEM2020:
    getEventsInMatch = sb.events(event)
    dfEventsEM2020 = pd.concat([dfEventsEM2020, getEventsInMatch])

for event in matchIdWM2022:
    getEventsInMatch = sb.events(event)
    dfEventsWM2022 = pd.concat([dfEventsWM2022, getEventsInMatch])

# set the key index
dfMatchesEM2020.set_index("match_id")
dfMatchesWM2022.set_index("match_id")



# reset the index, so a new index is created
dfEventsEM2020.reset_index(inplace=True)
dfEventsWM2022.reset_index(inplace=True)

# convert the dfEM2020 & dfWM2022 to a JSON.
# this is done for two reasons:
# 1) security: the provider can change the data all the time, in  downloading to JSON, we work on a hard copy
# 2) speed: it is way faster to work with data from a JSON file instead of always calling the API
# Therefore this code only has to be running once, the output is saved in a JSON file
dfEventsEM2020.to_json(
    'G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/JSON/BackUp/dfBackUpEventsEvaluationEM2020.json')
dfEventsWM2022.to_json(
    'G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/JSON/BackUp/dfBackUpEventsEvaluationWM2022.json')

#matches backup JSON
dfMatchesEM2020.to_json(
    'G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/JSON/BackUp/dfBackUpMatchesEvaluationEM2020.json')
dfMatchesWM2022.to_json(
    'G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/JSON/BackUp/dfBackUpMatchesEvaluationWM2022.json')


print("i am finished")