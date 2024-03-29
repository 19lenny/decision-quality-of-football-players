from statsbombpy import sb
import pandas as pd
from SetUp import DataManipulation, CONSTANTS
from tqdm import tqdm

"""
modelDF: prepare the dataset of all Competition, expect EM2020 & WM2022, such a model can be created from the data.
The dataset is manipulated, such that it only contains shots, and no other events.
Shots from penalties, free kicks and headers are not taken into account, since they distort the picture.
The dataset of the shot events is joined with the dataset of the according match.
Like this we have additional information about the game.
Additionally the dataset is manipulated, such that 4 additional rows are created (x, y, angle, distance).
Angle calculates the open angle from the striker to the goal.
Distance calculates the distance from the striker to the goal centre.
the manipulated dataset is saved in a JSON format.
"""

# save all competition and their season in a dictionary
dfComp = sb.competitions()
competitionIDs = dfComp.competition_id.values.tolist()
seasonIDs = dfComp.season_id.values.tolist()
print(competitionIDs)
print(seasonIDs)

# all data frames that are used in the for loop must be initialized
dfShotModelData = pd.DataFrame()
dfAllMatches = pd.DataFrame()
counter = 0
#set up
dfMatches = pd.DataFrame()
comp = []
seas = []
debugging = 0

# go through every season in every competition, except the one that are getting evaluated
for index in tqdm(range(len(competitionIDs)), colour='green'):


    # lets get all the matches of all seasons, except the ones we defined for our evaluation
    # EM2020: compID: 55, seasonID: 43
    # WM2022: compID: 43, seasonID: 106
    # WM2018: compID: 43, seasonID: 3

    currentCompetition = competitionIDs[index]
    currentSeason = seasonIDs[index]
    #print("progress bar getting the data for the model: ", index, "/", len(competitionIDs))
    try:
        if (currentCompetition != 55 or currentSeason != 43) and (currentCompetition != 43 or currentSeason != 106) and (currentCompetition != 43 or currentSeason != 3):
            #print("comp: ", currentCompetition, " season: ", currentSeason)
            # get all matches of the current competition / season
            dfMatches = pd.DataFrame(sb.matches(currentCompetition, currentSeason))
            # all MatchIDs of the current season
            matchIDs = dfMatches.match_id.values.tolist()

            # add this matches to a data frame, this is needed for additional information later during the join
            dfAllMatches = pd.concat([dfMatches, dfAllMatches])
            # set the key index for the join later
            dfMatches.set_index("match_id")

            # add all shot events, of every game, of every season in every competition, except the ones that are evaluated
            # here go through every event in every match
            for event in matchIDs:
                getEventsInMatch = sb.events(event)
                #print("i am still working, nothing to worry")
                # only keep the necessary rows,
                # which have something to do with shots and are not from penalties or freekicks, or straight corners
                getEventsInMatch = getEventsInMatch.query(
                    "type == 'Shot' & shot_body_part != 'Head' & shot_type == 'Open Play'")

                # add them to the current model
                dfShotModelData = pd.concat([dfShotModelData, getEventsInMatch])
                dfShotModelData.reset_index(drop=True, inplace=True)
                # add to every shot the current competition and current season
                debugging += 1

                # add the competition and the season for every event to a list
                for x in range(len(getEventsInMatch)):
                    comp.append(currentCompetition)
                    seas.append(currentSeason)

    except AttributeError:
        counter += 1
        print("fail counter: ", counter)
        print("data cannot be retrieved in comp: ", currentCompetition, " in season: ", currentSeason)

# join Shots and Matches
# therefore we know from every score the competition stage, the competition and additional information
dfModelData = dfShotModelData.join(dfAllMatches.set_index('match_id'), on='match_id')

# reset the index, so a new index is created
dfModelData.reset_index(drop=True, inplace=True)

# before we save the df, we want to add crucial information to the shot,
# with this information we can later create a better model
# therefore we calculate for every shot, the angle and the distance

# convert coordinates from list, to x and y entries
dfModelData = DataManipulation.coordinates(dfModelData)
# add angle
dfModelData = DataManipulation.angleDeg(dfModelData)
# add angle in rad
dfModelData = DataManipulation.angleInRadian(dfModelData)
#add the penalty for bad radians
dfModelData = DataManipulation.log_angle(dfModelData)
# add distance
dfModelData = DataManipulation.distancePlayerToGoal(dfModelData)
# binary solution of goal or no goal, so the model can easier be created
dfModelData = DataManipulation.addGoalBinary(dfModelData)

#add season and competition id
# add the competition and the season to the df
dfModelData['competition_id'] = comp
dfModelData['season_id'] = seas

# only keep the interesting columns

# reset the index, so a new index is created
dfModelData.reset_index(drop=True, inplace=True)

# convert the dfModelData to a JSON.
# this is done for two reasons:
# 1) security: the provider can change the data all the time, in  downloading to JSON, we work on a hard copy
# 2) speed: it is way faster to work with data from a JSON file instead of always calling the API
# Therefore this code only has to be running once, the output is saved in a JSON file

dfModelData.to_json("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/BackUp/TrainData/dfTrain_backup.json")


print("i am finished with downloading the training set")
