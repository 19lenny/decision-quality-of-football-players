# import all shots EM2020
from typing import List

from SetUp import JSONtoDF
import pandas as pd
import prepareDataframeScore
from scipy.stats import ttest_ind

dfEMScore = JSONtoDF.createDF("ScoreEM2020.json")


# make the tTest on this dataframes
dfWMScore = JSONtoDF.createDF("ScoreWM2022.json")


# concat df to 1 df to do tTest on it
dfScore = pd.concat([dfEMScore, dfWMScore])
dfScore = dfEMScore
dfScore.reset_index(drop=True, inplace=True)
print(dfScore['score'].abs())

# create empty lists, that can be filled later
shot_separation_range: List[int] = [0] * max(dfScore['score'].abs())
t_stat: List[float] = [0.0] * max(dfScore['score'].abs())
p_values: List[float] = [0.0] * max(dfScore['score'].abs())
len_df_in_front: List[int] = [0] * max(dfScore['score'].abs())
len_df_in_behind: List[int] = [0] * max(dfScore['score'].abs())

for shot_separation in range(max(dfScore['score'].abs())):
    print(shot_separation)
    #separate the dataframe according to the current shot separation
    dfInFront, dfInBehind = prepareDataframeScore.createInFrontInBehind(dfScore, shot_separation=shot_separation)
    #could be that it is empty, since no shots from the leading team were taken
    # therefore try as error handling
    try:
        shotValuesOne = dfInFront['xG_Delta_decision_alternative'].values.tolist()
        shotValuesTwo = dfInBehind['xG_Delta_decision_alternative'].values.tolist()

        t_stat[shot_separation], p_values[shot_separation] = ttest_ind(shotValuesOne, shotValuesTwo)
        shot_separation_range[shot_separation] = shot_separation
        len_df_in_front[shot_separation] = len(dfInFront['xG_Delta_decision_alternative'])
        len_df_in_behind[shot_separation] = len(dfInBehind['xG_Delta_decision_alternative'])
    except KeyError:
        len_df_in_behind[shot_separation] = len(dfInBehind['minute'])
        shot_separation_range[shot_separation] = shot_separation
        continue


dataScore = {'shot_separation': shot_separation_range,
                'T-stat': t_stat,
                'P-Val': p_values,
                'shots_in_front': len_df_in_front,
                'shots_in_behind': len_df_in_behind}
dfResult = pd.DataFrame(dataScore)
 # save the dataframe in a json like format
dfResult.to_json("tTest_score.json")

