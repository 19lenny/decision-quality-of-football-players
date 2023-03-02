from typing import List
from scipy.stats import ttest_ind
import pandas as pd
from SetUp import JSONtoDF, CONSTANTS


# the goal is only to evaluate teams that were represented in the group stage and in the knockout phase
# for this we have to manipulate the data a bit
def KOvsGroupStage(path_to_df, name_KO_stage):
    # first we do it for the EM 2020
    df = JSONtoDF.createDF(path_to_df)
    # create a dataframe with all teams that achieved the round of 16
    # this searches for the teams and drops all duplicates, since a team cannot achieve multiple time
    KO_stage = df[["home_team", "away_team"]][df['competition_stage'] == name_KO_stage].drop_duplicates()
    KO_stage = pd.concat([KO_stage['home_team'], KO_stage['away_team'].rename({'away_team': 'home_team'})])
    KO_stage = KO_stage.values.tolist()

    # keep only shots of teams that are in list of the round of 16
    dfManipulated = df[df['team'].isin(KO_stage)]
    dfManipulated.reset_index(inplace=True)
    dfManipulated.drop(["level_0", "index"], axis=1)
    return dfManipulated
