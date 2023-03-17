from typing import List

from scipy.stats import ttest_ind
from statistics import mean
import prepareDataframeStage
from SetUp import JSONtoDF, CONSTANTS
import pandas as pd

#EM 20

dfEM20 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONEM2020)
print(len(dfEM20['minute']))
dfResultEM20 = prepareDataframeStage.tTestResults(dfEM20)
# save the dataframe in a json like format
dfResultEM20.to_json("results/tTest_competition_stage_vs_other_stages_EM20.json")

#WM 22

dfWM22 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONWM2022)
print(len(dfWM22['minute']))
dfResultWM22 = prepareDataframeStage.tTestResults(dfWM22)
# save the dataframe in a json like format
dfResultWM22.to_json("results/tTest_competition_stage_vs_other_stages_WM22.json")

# EM and WM together

# the df are bundled together because the evaluation is done for both df
dfComp = pd.concat([dfEM20, dfWM22])
print(len(dfComp['minute']))
dfComp.reset_index(drop=True, inplace=True)
dfResultComp = prepareDataframeStage.tTestResults(dfComp)
# save the dataframe in a json like format
dfResultComp.to_json("results/tTest_competition_stage_vs_other_stages_competitions.json")


