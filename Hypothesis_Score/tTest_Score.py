# import all shots EM2020
from typing import List

from SetUp import JSONtoDF
import pandas as pd
import prepareDataframeScore
from scipy.stats import ttest_ind

# make the tTest on this dataframe
dfEMScore = JSONtoDF.createDF("ScoreEM2020.json")
dfEMScoreResult = prepareDataframeScore.tTestExecution(dfScore=dfEMScore)
 # save the dataframe in a json like format
dfEMScoreResult.to_json("results/tTest_score_EM20.json")

# make the tTest on this dataframe
dfWMScore = JSONtoDF.createDF("ScoreWM2022.json")
dfWMScoreResult = prepareDataframeScore.tTestExecution(dfScore=dfWMScore)
dfWMScoreResult.to_json("results/tTest_score_WM22.json")


# concat df to 1 df to do tTest on it
dfScore = pd.concat([dfEMScore, dfWMScore])
dfAllCompetitionsResult = prepareDataframeScore.tTestExecution(dfScore=dfScore)
dfAllCompetitionsResult.to_json("results/tTest_score_all_competitions.json")




