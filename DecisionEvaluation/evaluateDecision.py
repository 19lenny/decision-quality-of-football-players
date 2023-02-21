from SetUp import JSONtoDF, DataManipulation, CONSTANTS
import pandas as pd
import json
import os

from DecisionEvaluation import offside


# it has to be checked why distance is farther away as it should be
df = JSONtoDF.createDF(CONSTANTS.JSONEM2020)
x = df['x_coordinate'].mean()
y = df['y_coordinate'].mean()
dist = df['distance_to_goal_centre'].mean()

# for every shot of the competition
# this for loop gets every shot from a competition, starting with the first shot
for row in range(len(df)):

    # get all players that were in the frame during the current shot
    # the dataframe contains a json like format
    # this has to be transformed to a dataframe

    # get the players
    jsonOtherPlayers = df['shot_freeze_frame'][row]
    # transform it to a real json
    jsonOtherPlayers = json.dumps(jsonOtherPlayers)
    # save the json (name = sample.json, so we can import it to a dataframe
    with open("sample.json", "w") as outfile:
        outfile.write(jsonOtherPlayers)

    # import it to a dataframe
    # this dataframe contains all data from all players that were in the frame during the shot
    dfOtherPlayers = pd.read_json('sample.json')

    # sample.json is no longer needed and can be deleted
    # clean up
    filename = "sample.json"
    os.remove(CONSTANTS.JSONDECEVA + filename)

    # for better readability are the x and y coordinates changed from a list setting to single rows
    dfOtherPlayers = DataManipulation.coordinates(dfOtherPlayers)

    # the id and the name of the players which were in the frame during the shot are in a dictionary
    # this has to be transformed to rows

    # create empty lists, they symbolize the rows, which are filled in the next for loop
    idOtherPlayer = []
    name = []
    # go through every player that was in the shot...
    for rowPlayers in range(len(dfOtherPlayers['player'])):
        # ...and add his personal id to a list
        idOtherPlayer.append(dfOtherPlayers['player'][rowPlayers]['id'])
        # ...and add his name to a list
        name.append(dfOtherPlayers['player'][rowPlayers]['name'])

    # the lists that were created before are now transformed back rows
    dfOtherPlayers['id'] = idOtherPlayer
    dfOtherPlayers['name'] = name

    # now the dataset is ready to check if the player originally made a good decision with shooting

    # get the calculated xG value for the current shot
    shootingPlayerxG = df['xGAngleDistance'][row]
    x_shooting_player = df['x_coordinate'][row]
    y_shooting_player = df['x_coordinate'][row]

    # where is the offside line for this shot
    offside_x = offside.offsideLine(x_shooting_player, dfOtherPlayers)
    # update the dataframe to see who is offside
    dfOtherPlayers = offside.isOffside(offside_x, dfOtherPlayers)
    # players in the opponent team cannot be offside, but players in the own team
    # if the players in the own team are offside, they cannot be passed to

    # todo: go through the whole pitch, check every square and give pass probability


