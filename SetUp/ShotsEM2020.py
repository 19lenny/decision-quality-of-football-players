from statsbombpy import sb
import pandas as pd
from SetUp import DataManipulation, CONSTANTS

"""
DfEM2020: prepare the dataset of EM2020, such it can be evaluated.
The dataset is manipulated, such that it only contains shots, and no other events.
Shots from penalties, free kicks and headers are not taken into account, since they distort the picture.
The dataset of the shot events is joined with the dataset of the according match.
Like this we have additional information about the game.
Additionally the dataset is manipulated, such that 4 additional rows are created (x, y, angle, distance).
Angle calculates the open angle from the striker to the goal.
Distance calculates the distance from the striker to the goal centre.
the manipulated dataset is saved in a JSON format.
"""

# 55,43 is the code of the EM 2020. This can be found in the excel overview "CompetitionOverview.xlsx"
dfMatchesEM2020 = pd.DataFrame(sb.matches(55, 43))

# all matchID's EM2020
matchIdEM2020 = dfMatchesEM2020.match_id.values.tolist()

# initialize df
dfShotEM2020 = pd.DataFrame()

# this must be done for every event in every game,
# then we have a dataframe with all shots from every game from the EM2020
counter = 0
for event in matchIdEM2020:
    getEventsInMatch = sb.events(event)
    # only keep the necessery rows, which have something to do with shots and are not from penalties or freekicks
    getEventsInMatch = getEventsInMatch.query(
        "type == 'Shot' ")
    dfShotEM2020 = pd.concat([dfShotEM2020, getEventsInMatch])
    counter += 1
    print("nothing to worry - still working")
    print("progress bar: ", counter, " / ", len(matchIdEM2020))

# set the key index for the join later
dfMatchesEM2020.set_index("match_id")

# join Shots and Matches, therefore we know from every score the compettion stage,
# the competition and additional information
dfEM2020 = dfShotEM2020.join(dfMatchesEM2020.set_index('match_id'), on='match_id')

# before we save the df, we want to add crucial information to the shot,
# with this information we can later calculate the xG
# therefore we calculate for every shot, the angle and the distance

# convert coordinates from list, to x and y entries
dfEM2020 = DataManipulation.coordinates(dfEM2020)
# add angle
dfEM2020 = DataManipulation.angle(dfEM2020)
# add angle in rad
dfEM2020 = DataManipulation.angleInRadian(dfEM2020)
# add distance
dfEM2020 = DataManipulation.distancePlayerToGoal(dfEM2020)
#add goal
dfEM2020 = DataManipulation.addGoalBinary(dfEM2020)


# save only the needed columns
dfEM2020 = dfEM2020[
    ["x_coordinate", "y_coordinate", "shot_end_location", "shot_outcome", "angle", "angleInRadian", "distance_to_goal_centre",
     "shot_statsbomb_xg", "goal", "match_id", "shot_body_part", "period",
     "team", "play_pattern", "minute", "player", "shot_freeze_frame", "shot_type", "match_date", "competition",
     "season", "home_team", "away_team", "home_score", "away_score", "competition_stage"]]

# reset the index, so a new index is created
dfEM2020.reset_index(inplace=True)

# convert the dfEM2020 to a JSON.
# this is done for two reasons:
# 1) security: the provider can change the data all the time, in  downloading to JSON, we work on a hard copy
# 2) speed: it is way faster to work with data from a JSON file instead of always calling the API
# Therefore this code only has to be running once, the output is saved in a JSON file
dfEM2020.to_json("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Hypothesis_Score/ShotsEM2020.json")

print("i am finished")
