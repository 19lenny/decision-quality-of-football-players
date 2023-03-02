from typing import List
from scipy.stats import ttest_ind
import pandas as pd
from SetUp import JSONtoDF, CONSTANTS

# H0: the decision in the first x minutes to the last 90-x minutes have no difference
# reject H0 if pval < alpha

# first add WM 22 and EM 20 to one dataframe together
dfEM20 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONEM2020)
dfWM22 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONWM2022)

dfShotEval = pd.concat([dfEM20, dfWM22])

# create empty lists, that can be filled later
t_stat: List[float] = [0.0] * max(dfShotEval['minute'][dfShotEval['period'] == 2])
p_values: List[float] = [0.0] * max(dfShotEval['minute'][dfShotEval['period'] == 2])
min: List[int] = [0] * max(dfShotEval['minute'][dfShotEval['period'] == 2])
meanOne: List[float] = [0.0] * max(dfShotEval['minute'][dfShotEval['period'] == 2])
meanTwo: List[float] = [0.0] * max(dfShotEval['minute'][dfShotEval['period'] == 2])

# for every minute in a game check, if it makes a difference if we compare the two groups
for minute in range(max(dfShotEval['minute'][dfShotEval['period'] == 2])):
    # split the dataframe in two groups, first group is the first x minute df, second group is the 90-minute dataframe
    # the +1 has to be done because python counts from 0, but the first minute in a football game is 1

    # we have to check some special cases
    # minute 45 can happen in period 1 or 2
    if minute + 1 == 45:
        dfShotEvalOne = dfShotEval.loc[
            (dfShotEval['minute'] <= minute + 1) & (dfShotEval['period'] == 1)]
        dfShotEvalTwo = dfShotEval.loc[
            (dfShotEval['minute'] >= minute + 1) & (dfShotEval['period'] == 2)]
    # minute 90 can happen in period 2 or 3, therefore always check if minute is in 1 or 2
    else:
        dfShotEvalOne = dfShotEval.loc[
            (dfShotEval['minute'] <= minute + 1) & ((dfShotEval['period'] == 1) | (dfShotEval['period'] == 2))]
        # we only want to compare to the 90 th minute, additional time shouldnt play a role here
        dfShotEvalTwo = dfShotEval.loc[(dfShotEval['minute'] > minute + 1) & (
                    (dfShotEval['period'] == 1) | (dfShotEval['period'] == 2))]
    x = dfShotEvalOne['xG_Delta_decision_alternative'].mean()
    meanOne[minute] = dfShotEvalOne['xG_Delta_decision_alternative'].mean()

    # create a list out of the dataframes
    shotValuesOne = dfShotEvalOne['xG_Delta_decision_alternative'].values.tolist()
    shotValuesTwo = dfShotEvalTwo['xG_Delta_decision_alternative'].values.tolist()
    meanTwo[minute] = dfShotEvalTwo['xG_Delta_decision_alternative'].mean()
    # add the minutes to a list
    # the +1 has to be done because python counts from 0, but the first minute in a football game is 1
    min[minute] = minute + 1
    # calculate the t-test statistics for the current minute
    t_stat[minute], p_values[minute] = ttest_ind(shotValuesOne, shotValuesTwo)

# save the created lists to a dataframe
dataTime = {'minute': min,
            'T-stat': t_stat,
            'P-Val': p_values,
            'mean_low_minute': meanOne,
            'mean_high_minute': meanTwo}
dfTime = pd.DataFrame(dataTime)
# save the dataframe in a json like format
dfTime.to_json("tTest_time90_results.json")

# create empty lists, that can be filled later
t_stat: List[float] = [0.0] * (max(dfShotEval['minute'][dfShotEval['period'] == 4])-90)
p_values: List[float] = [0.0] * (max(dfShotEval['minute'][dfShotEval['period'] == 4])-90)
min: List[int] = [0] * (max(dfShotEval['minute'][dfShotEval['period'] == 4])-90)
meanOne: List[float] = [0.0] * (max(dfShotEval['minute'][dfShotEval['period'] == 4])-90)
meanTwo: List[float] = [0.0] * (max(dfShotEval['minute'][dfShotEval['period'] == 4])-90)
index = 0
# additional time
for minute in range(90, max(dfShotEval['minute'])):
    # split the dataframe in two groups, first group is the first x minute df, second group is the 90-minute dataframe
    # the +1 has to be done because python counts from 0, but the first minute in a football game is 1

    # we have to check some special cases
    # minute 45 can happen in period 1 or 2
    if minute + 1 == 105:
        dfShotEvalOne = dfShotEval.loc[
            (dfShotEval['minute'] <= minute + 1) & (dfShotEval['period'] == 3)]
        dfShotEvalTwo = dfShotEval.loc[
            (dfShotEval['minute'] >= minute + 1) & (dfShotEval['period'] == 4)]
    # minute 90 can happen in period 2 or 3, therefore always check if minute is in 1 or 2
    else:
        dfShotEvalOne = dfShotEval.loc[
            (dfShotEval['minute'] <= minute + 1) & ((dfShotEval['period'] == 3) | (dfShotEval['period'] == 4))]
        # we only want to compare to the 90 th minute, additional time shouldnt play a role here
        dfShotEvalTwo = dfShotEval.loc[(dfShotEval['minute'] > minute + 1) & (
                (dfShotEval['period'] == 3) | (dfShotEval['period'] == 4))]
    meanOne[index] = dfShotEvalOne['xG_Delta_decision_alternative'].mean()

    # create a list out of the dataframes
    shotValuesOne = dfShotEvalOne['xG_Delta_decision_alternative'].values.tolist()
    shotValuesTwo = dfShotEvalTwo['xG_Delta_decision_alternative'].values.tolist()
    meanTwo[index] = dfShotEvalTwo['xG_Delta_decision_alternative'].mean()
    # add the minutes to a list
    # the +1 has to be done because python counts from 0, but the first minute in a football game is 1
    min[index] = minute + 1
    # calculate the t-test statistics for the current minute
    t_stat[index], p_values[index] = ttest_ind(shotValuesOne, shotValuesTwo)
    index += 1

    # save the created lists to a dataframe
    dataTime120 = {'minute': min,
                'T-stat': t_stat,
                'P-Val': p_values,
                'mean_low_minute': meanOne,
                'mean_high_minute': meanTwo}
    dfTime120 = pd.DataFrame(dataTime120)
    # save the dataframe in a json like format
    dfTime120.to_json("tTest_time90_120_results.json")