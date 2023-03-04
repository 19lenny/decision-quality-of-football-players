from typing import List

from scipy.stats import ttest_ind
from statistics import mean
import prepareDataframe
from SetUp import JSONtoDF, CONSTANTS
import pandas as pd

# the first calculations are done excluding "3rd Place Final", since this is a strange final
ko_stages = ["Round of 16", "Quarter-finals", "Semi-finals", "Final"]

# create empty lists, that can be filled later
t_stat: List[float] = [0.0] * len(ko_stages)
p_values: List[float] = [0.0] * len(ko_stages)
current_highest_stage: List[str] = [''] * len(ko_stages)
meanOne: List[float] = [0.0] * len(ko_stages)
meanTwo: List[float] = [0.0] * len(ko_stages)

# H0: the competitors of the current highest competition stage
# have done the same decision in the upcoming competition stages compared to the played ones before
for index in range(len(ko_stages)):

    # we manipulate the dataframes in a way that only the shots of the teams count,
    # that achieved the current highest competition round
    dfEM20 = prepareDataframe.KOvsGroupStage(CONSTANTS.JSONSHOTEVALUATIONEM2020, ko_stages[index])
    dfWM22 = prepareDataframe.KOvsGroupStage(CONSTANTS.JSONSHOTEVALUATIONWM2022, ko_stages[index])
    # the df are bundled together because the evaluation is done for both df
    dfShotEval = pd.concat([dfEM20, dfWM22])

    # create group stage df and transform it to a list
    # when the list is empty then we are not in the ko stages, than the comparable stage is only the group stage

    current_stages_df = dfShotEval.loc[dfShotEval['competition_stage'] == "Group Stage"]

    shotValuesCurrentStages = current_stages_df['xG_Delta_decision_alternative'].values.tolist()
    x = len(shotValuesCurrentStages)
    meanOne[index] = mean(shotValuesCurrentStages)

    # create df for all remaining knock out stages and create a list from it
    ko_stage_df = dfShotEval.loc[dfShotEval['competition_stage'].isin(ko_stages[index:])]
    shotValuesRemainingStages = ko_stage_df['xG_Delta_decision_alternative'].values.tolist()
    y = len(shotValuesRemainingStages)
    meanTwo[index] = mean(shotValuesRemainingStages)

    t_stat[index], p_values[index] = ttest_ind(shotValuesCurrentStages, shotValuesRemainingStages)
    current_highest_stage[index] = ko_stages[index]


# save the created lists to a dataframe
dataCompetitionStage = {'competition_separator': current_highest_stage,
            'T-stat': t_stat,
            'P-Val': p_values,
            'mean_low_competition': meanOne,
            'mean_high_competition': meanTwo}
dfCompStage = pd.DataFrame(dataCompetitionStage)
# save the dataframe in a json like format
dfCompStage.to_json("tTest_competition_stage_vs_group_stage_results.json")

