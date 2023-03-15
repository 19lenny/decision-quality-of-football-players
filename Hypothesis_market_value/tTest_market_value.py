# import all shots EM2020
from typing import List
import re
from SetUp import JSONtoDF, CONSTANTS
import pandas as pd
import ws_tm_values
from scipy.stats import ttest_ind
import ws_tm_values
from difflib import SequenceMatcher

#dfWMValues = ws_tm_values.transfermarketValue("WM")
#dfWMValues.to_json("ValuesWM.json")
dfWMValues = JSONtoDF.createDF("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Hypothesis_market_value/ValuesWM.json")

# dfEMValues = ws_tm_values.transfermarketValue("EM")

dfEM20 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONEM2020)
dfWM22 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONWM2022)
# since the statsbomb names contains 3rd ant 4th names and transfermarkt names does not contain these names,
# the join operator has to be built manually
dfWM22 = ws_tm_values.join(dfCompetition=dfWM22, dfValues=dfWMValues)


#dfEMValues = ws_tm_values.transfermarketValue("EM")
#dfEMValues.to_json("ValuesEM.json")
dfEMValues = JSONtoDF.createDF("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Hypothesis_market_value/ValuesEM.json")
dfEM20 = ws_tm_values.join(dfCompetition=dfEM20, dfValues=dfEMValues)

q = dfEM20['value'].quantile([0.25, 0.5, 0.75])
mean = dfEM20['value'].median()

