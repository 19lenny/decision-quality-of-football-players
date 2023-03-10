# import all shots EM2020
from SetUp import JSONtoDF
import pandas as pd
import prepareDataframeScore
from scipy.stats import ttest_ind

dfEMScore = JSONtoDF.createDF("ScoreEM2020.json")
# throw away unnecessary shots like penalties and headers and freekicks
dfEMScore = dfEMScore.query("shot_body_part != 'Head' & play_pattern != 'From Free Kick' & shot_type != 'Penalty'")

# make the tTest on this dataframes
dfWMScore = JSONtoDF.createDF("ScoreWM2022.json")
dfWMScore = dfWMScore.query("shot_body_part != 'Head' & play_pattern != 'From Free Kick' & shot_type != 'Penalty'")

# concat df to 1 df to do tTest on it
dfScore = pd.concat([dfWMScore, dfEMScore])
dfScore.reset_index(drop=True, inplace=True)

dfInFront, dfInBehind = prepareDataframeScore.prepDF(dfScore, shot_separation=0)

shotValuesOne = dfInFront['xG_Delta_decision_alternative'].values.tolist()
shotValuesTwo = dfInBehind['xG_Delta_decision_alternative'].values.tolist()
tStat, pValue = ttest_ind(shotValuesOne, shotValuesTwo)

print(tStat, pValue)
