import pandas as pd
from SetUp import JSONtoDF, CONSTANTS, DataManipulation


def createInFrontInBehind(dfScore, shot_separation):
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
        shot_separation_home = shot_separation
        # shot separation away is created, since if an away team is leading, the score will be negative
        shot_separation_away = shot_separation*-1
        # the shooting team is home team, and the home team is in front, with a distance of shot separation
        if (shooting_team == home_team) & (score >= shot_separation_home):
            dfUp = pd.concat(axis=1, objs=[dfUp, dfScore.iloc[shot]])
        # the shooting team is away team, and the away team is in front
        # score must be smaller than shot separation, since
        # if away scores it is -1, if away is in front the score is negative
        elif (shooting_team == away_team) & (score <= shot_separation_away):
            # the axis are on the wrong side, therefore the concat method has to given the option to switch the axis
            # in the end this is fixed by transpose the axis
            dfUp = pd.concat(axis=1, objs=[dfUp, dfScore.iloc[shot]])
        elif (shooting_team == home_team) & (score < shot_separation_home):
            dfDown = pd.concat(axis=1, objs=[dfDown, dfScore.iloc[shot]])
        elif (shooting_team == away_team) & (score > shot_separation_away):
            dfDown = pd.concat(axis=1, objs=[dfDown, dfScore.iloc[shot]])
    dfUp = dfUp.transpose()
    dfUp.reset_index(drop=True, inplace=True)
    # dfUp = dfUp.drop(columns=['level_0', 'index'])
    dfDown = dfDown.transpose()
    dfDown.reset_index(drop=True, inplace=True)
    # dfDown = dfDown.drop(columns=['level_0', 'index'])

    return dfUp, dfDown
