from typing import List
from scipy.stats import ttest_ind
import pandas as pd
from SetUp import JSONtoDF, CONSTANTS

# H0: the decision in the first x minutes to the last 90-x minutes have no difference

# first add WM 22 and EM 20 to one dataframe together
dfEM20 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONEM2020)
dfWM22 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONWM2022)

dfShotEval = pd.concat([dfEM20, dfWM22])


# create empty lists, that can be filled later
t_stat: List[float] = [0.0] * 90
p_values: List[float] = [0.0] * 90
min: List[int] = [0] * 90
meanOne: List[float] = [0.0] * 90
meanTwo: List[float] = [0.0] * 90


# for every minute in a game check, if it makes a difference if we compare the two groups
for minute in range(90):
    # split the dataframe in two groups, first group is the first x minute df, second group is the 90-minute dataframe
    # the +1 has to be done because python counts from 0, but the first minute in a football game is 1
    dfShotEvalOne = dfShotEval.loc[dfShotEval['minute'] <= minute+1]
    dfShotEvalTwo = dfShotEval.loc[dfShotEval['minute'] > minute+1]

    # create a list out of the dataframes
    shotValuesOne = dfShotEvalOne['xG_Delta_decision_alternative'].values.tolist()
    shotValuesTwo = dfShotEvalTwo['xG_Delta_decision_alternative'].values.tolist()
    # add the minutes to a list
    # the +1 has to be done because python counts from 0, but the first minute in a football game is 1
    min[minute] = minute+1
    # calculate the t-test statistics for the current minute
    t_stat[minute], p_values[minute] = ttest_ind(shotValuesOne, shotValuesTwo)

# save the created lists to a dataframe
dataTime = {'minute': min,
            'T-stat': t_stat,
            'P-Val': p_values}
dfTime = pd.DataFrame(dataTime)
# save the dataframe in a json like format
dfTime.to_json("tTest_results.json")
