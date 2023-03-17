from typing import List

import pandas as pd
from SetUp import JSONtoDF, CONSTANTS, DataManipulation
from scipy.stats import ttest_ind


def createInFrontInBehind(dfScore, score_separation):
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
        score_separation_home = score_separation
        # shot separation away is created, since if an away team is leading, the score will be negative
        score_separation_away = score_separation * -1
        # the shooting team is home team, and the home team is in front, with a distance of shot separation
        if (shooting_team == home_team) & (score >= score_separation_home):
            dfUp = pd.concat(axis=1, objs=[dfUp, dfScore.iloc[shot]])
        # the shooting team is away team, and the away team is in front
        # score must be smaller than shot separation, since
        # if away scores it is -1, if away is in front the score is negative
        elif (shooting_team == away_team) & (score <= score_separation_away):
            # the axis are on the wrong side, therefore the concat method has to given the option to switch the axis
            # in the end this is fixed by transpose the axis
            dfUp = pd.concat(axis=1, objs=[dfUp, dfScore.iloc[shot]])
        elif (shooting_team == home_team) & (score < score_separation_home):
            dfDown = pd.concat(axis=1, objs=[dfDown, dfScore.iloc[shot]])
        elif (shooting_team == away_team) & (score > score_separation_away):
            dfDown = pd.concat(axis=1, objs=[dfDown, dfScore.iloc[shot]])
    dfUp = dfUp.transpose()
    dfUp.reset_index(drop=True, inplace=True)
    # dfUp = dfUp.drop(columns=['level_0', 'index'])
    dfDown = dfDown.transpose()
    dfDown.reset_index(drop=True, inplace=True)
    # dfDown = dfDown.drop(columns=['level_0', 'index'])

    return dfUp, dfDown

def tTestExecution(dfScore):
    # first reset the indexof the current dataframe
    # this is done, to ensure that the for loop works properly
    dfScore.reset_index(drop=True, inplace=True)

    # create empty lists, that can be filled later
    score_separation_range: List[int] = [0] * max(dfScore['score'].abs())
    t_stat: List[float] = [0.0] * max(dfScore['score'].abs())
    p_values: List[float] = [0.0] * max(dfScore['score'].abs())
    len_df_in_front: List[int] = [0] * max(dfScore['score'].abs())
    len_df_in_behind: List[int] = [0] * max(dfScore['score'].abs())

    # separate the dataframes from a draw (score_separation = 0) to the highest scoring difference of a game (=max(dfScore['score'].abs()))
    # score_separation = 0 --> inFront every shot that is shot, while not loosing, inBehind every shot that is shot while loosing
    # score_separation = 1 --> inFront every shot that is shot, while winning with at least 1 up, inBehind every shot that is shot while loosing or drawing
    # score_separation = 2 --> inFront every shot that is shot, while winning with at least 2 up, inBehind every shot that is shot while loosing or drawing or winning teams that are up by 1 difference
    # and so on
    for score_separation in range(max(dfScore['score'].abs())):
        # in which shot separation are we
        # separate the dataframe according to the current shot separation
        dfInFront, dfInBehind = createInFrontInBehind(dfScore, score_separation=score_separation)
        # could be that it is empty, since no shots from the leading team were taken
        # therefore try as error handling
        try:
            shotScoreLow = dfInFront['xG_Delta_decision_alternative'].values.tolist()
            shotScoreHigh = dfInBehind['xG_Delta_decision_alternative'].values.tolist()

            t_stat[score_separation], p_values[score_separation] = ttest_ind(shotScoreLow, shotScoreHigh)
            score_separation_range[score_separation] = score_separation
            len_df_in_front[score_separation] = len(dfInFront['xG_Delta_decision_alternative'])
            len_df_in_behind[score_separation] = len(dfInBehind['xG_Delta_decision_alternative'])
        except KeyError:
            len_df_in_behind[score_separation] = len(dfInBehind['minute'])
            score_separation_range[score_separation] = score_separation
            continue

    dataScore = {'score_separation': score_separation_range,
                 'T-stat': t_stat,
                 'P-Val': p_values,
                 'number_shots_in_front': len_df_in_front,
                 'number_shots_in_behind': len_df_in_behind}
    dfResult = pd.DataFrame(dataScore)
    return dfResult