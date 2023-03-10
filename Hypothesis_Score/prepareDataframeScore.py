import pandas as pd
from SetUp import JSONtoDF, CONSTANTS, DataManipulation

def addXG(dfScore):
    #todo: vgl evalDecIntercEM2020
def addXGDifference(dfScore):
    #todo: vgl evalDecIntercEM2020


def prepDF(dfScore, shot_separation):
    # df Up describes the dataframe, in which all shots are shooted where the shooting team is in front,
    # with scoring difference as defined above
    dfUp = pd.DataFrame()
    # df down describes the dataframe, in which all shots are shooted where the shooting team is in behind
    # or is playing on a draw,
    # with scoring difference as defined above
    dfDown = pd.DataFrame()

    for shot in range(len(dfScore)):
        shooting_team = dfScore['team'][shot]
        home_team = dfScore['home_team'][shot]
        away_team = dfScore['away_team'][shot]
        score = dfScore['score'][shot]
        # the shooting team is home team, and the home team is in front
        if (shooting_team == home_team) & (score > shot_separation):
            dfUp = pd.concat(axis=1, objs=[dfUp, dfScore.iloc[shot]])
        # the shooting team is away team, and the away team is in front
        # score must be smaller than shot separation, since
        # if away scores it is -1, if away is in front the score is negative
        elif (shooting_team == away_team) & (score < shot_separation):
            dfUp = pd.concat(axis=1, objs=[dfUp, dfScore.iloc[shot]])
        elif (shooting_team == home_team) & (score <= shot_separation):
            dfDown = pd.concat(axis=1, objs=[dfDown, dfScore.iloc[shot]])
        elif (shooting_team == away_team) & (score >= shot_separation):
            dfDown = pd.concat(axis=1, objs=[dfDown, dfScore.iloc[shot]])
    dfUp = dfUp.transpose()
    dfUp.reset_index(drop=True, inplace=True)
    dfUp = dfUp.drop(columns=['level_0', 'index'])
    dfDown = dfDown.transpose()
    dfDown.reset_index(drop=True, inplace=True)
    dfDown = dfDown.drop(columns=['level_0', 'index'])
    return dfUp, dfDown


print("deb")
