from statsbombpy import sb
import pandas as pd
import DataManipulationAngleDistance

# 43,106 is the code of the WM 2022. This can be found in the excel overview "CompetitionOverview.xlsx"
dfMatchesWM2022 = pd.DataFrame(sb.matches(43, 106))

# all matchID's WM2022
matchIdWM2022 = dfMatchesWM2022.match_id.values.tolist()

# initialize df
dfShotWM2022 = pd.DataFrame()

# this must be done for every event in every game, then we have a dataframe with all shots from every game from the WM2022
for event in matchIdWM2022:
    getEventsInMatch = sb.events(event)
    # only keep the necessery rows, which have something to do with shots and are not from penalties or freekicks
    getEventsInMatch = getEventsInMatch.query(
        "type == 'Shot' & shot_body_part != 'Head' & play_pattern != 'From Free Kick' & shot_type != 'Penalty'")
    dfShotWM2022 = pd.concat([dfShotWM2022, getEventsInMatch])

# set the key index for the join later
dfMatchesWM2022.set_index("match_id")

# join Shots and Matches, therefore we know from every score the compettion stage, the competition and additional information
dfWM2022 = dfShotWM2022.join(dfMatchesWM2022.set_index('match_id'), on='match_id')

# before we save the df, we want to add crucial information to the shot, with this information we can later calculate the xG
# therefore we calculate for every shot, the angle and the distance

# convert coordinates from list, to x and y entries
dfWM2022 = DataManipulationAngleDistance.coordinates(dfWM2022)
# add angle
dfWM2022 = DataManipulationAngleDistance.angle(dfWM2022)
# add distance
dfWM2022 = DataManipulationAngleDistance.distance(dfWM2022)

# save only the needed columns
dfWM2022 = dfWM2022[
    ["x_coordinate", "y_coordinate", "shot_end_location", "shot_outcome", "angle", "distance_to_goal_centre",
     "shot_statsbomb_xg", "match_id", "shot_body_part", "period",
     "team", "play_pattern", "minute", "player", "shot_freeze_frame", "shot_type", "match_date", "competition",
     "season", "home_team", "away_team", "home_score", "away_score", "competition_stage"]]

# reset the index, so a new index is created
dfWM2022.reset_index(inplace=True)

# convert the dfEM2020 to a JSON.
# this is done for two reasons:
# 1) security: the provider can change the data all the time, in  downloading to JSON, we work on a hard copy
# 2) speed: it is way faster to work with data from a JSON file instead of always calling the API
# Therefore this code only has to be running once, the output is saved in a JSON file
dfWM2022.to_json('G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/JSON/ShotsWM2022.json')

print("i am finished")