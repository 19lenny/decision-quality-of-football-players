from SetUp import JSONtoDF, DataManipulation, CONSTANTS
import pandas as pd
import json
import os
import numpy as np
from DecisionEvaluation import evaluationHelper
from SetUp import CONSTANTS, JSONtoDF
import pandas as pd
from Model import  model


# todo: it has to be checked why distance is farther away as it should be
df = JSONtoDF.createDF(CONSTANTS.JSONEM2020)
x = df['x_coordinate'].mean()
y = df['y_coordinate'].mean()
dist = df['distance_to_goal_centre'].mean()
shot = df[(df['match_id'] == 3795220) & (df['player'] == 'Ciro Immobile')]


def getPlayersOfEventA(shot):
    # transform players which are in the shot from a json like format to a dataframe format

    # the event comes in a json like format
    # transform it to a real json
    jsonOtherPlayers = json.dumps(shot)
    # save the json (name = sample.json), so we can import it to a dataframe
    filename = "sampleaaa.json"
    with open(filename, "w") as outfile:
        outfile.write(jsonOtherPlayers)

    # import it to a dataframe
    # this dataframe contains all data from all players that were in the frame during the shot
    dfOtherPlayers = pd.read_json(filename)

    # clean up
    # sample.json is no longer needed and can be deleted
    os.remove(filename)

    # the player_id, the player_name, the position_id and the position name have in the df still a dictionary like format
    # change this, such that id and name are additional columns in the dataframe

    # create empty lists, they symbolize the rows, which are filled in the next for loop
    idOtherPlayer = []
    nameOtherPlayer = []
    idPosition = []
    namePosition = []
    # go through every player that was in the shot...
    for rowPlayers in range(len(dfOtherPlayers['player'])):
        # ...and add his personal id to a list
        idOtherPlayer.append(dfOtherPlayers['player'][rowPlayers]['id'])
        # ...and add his name to a list
        nameOtherPlayer.append(dfOtherPlayers['player'][rowPlayers]['name'])
        # ...and add his position id to a list
        idPosition.append(dfOtherPlayers['position'][rowPlayers]['id'])
        # ...and add the position name to a list
        namePosition.append(dfOtherPlayers['position'][rowPlayers]['name'])

    # the lists that were created before are now transformed back rows
    dfOtherPlayers['id_player'] = idOtherPlayer
    dfOtherPlayers['name_player'] = nameOtherPlayer
    dfOtherPlayers['id_position'] = idPosition
    dfOtherPlayers['name_position'] = namePosition

    # the x and x coordinates of each player have in the df still a list like format
    # change this, such that x and a are additional columns in the dataframe

    # for better readability are the x and y coordinates changed from a list setting to single rows setting in the df
    dfOtherPlayers = DataManipulation.coordinates(dfOtherPlayers)

    # remove the columns which have a dictionary / list like format
    dfOtherPlayers = dfOtherPlayers.drop(columns=["location", "player", "position"])

    # dataframe of every player in the freeze frame is prepared: return the df
    return dfOtherPlayers

dfOtherPlayers = getPlayersOfEventA(shot['shot_freeze_frame'][37])



"""
x_location = 114
y_location = 40
logmodel = CONSTANTS.REGMODELINTERC

angle_in_rad = DataManipulation.angleInRadianFromObjectToPoints(x_object=x_location, y_object=y_location,
                                                                x_point1=CONSTANTS.X_COORDINATE_POST1,
                                                                y_point1=CONSTANTS.Y_COORDINATE_POST1,
                                                                x_point2=CONSTANTS.X_COORDINATE_POST2,
                                                                y_point2=CONSTANTS.Y_COORDINATE_POST2)
distance_in_yards = DataManipulation.distanceObjectToPoint(x_object=x_location, y_object=y_location,
                                                           x_point=CONSTANTS.X_COORDINATE_GOALCENTRE,
                                                           y_point=CONSTANTS.Y_COORDINATE_GOALCENTRE)
prediction = model.predictionOfSingleValues([angle_in_rad, distance_in_yards], CONSTANTS.ATTRIBUTES, logmodel)
predictionNOIntercept = model.predictionOfSingleValues([angle_in_rad, distance_in_yards], CONSTANTS.ATTRIBUTES, CONSTANTS.REGMODELNOINTERC)


model.show_info(CONSTANTS.REGMODELINTERC)
model.show_info(CONSTANTS.REGMODELNOINTERC)

"""


