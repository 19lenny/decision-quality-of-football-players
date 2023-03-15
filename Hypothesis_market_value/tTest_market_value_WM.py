# import all shots EM2020
from typing import List
import re
from SetUp import JSONtoDF, CONSTANTS
import pandas as pd
import ws_tm_values
from scipy.stats import ttest_ind
import ws_tm_values
from difflib import SequenceMatcher

# dfWMValues = ws_tm_values.transfermarketValue("WM")
# dfWMValues.to_json("ValuesWM.json")
dfWM22 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONWM2022)
dfWMValues = JSONtoDF.createDF("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Hypothesis_market_value/ValuesWM.json")

# since the statsbomb names contains 3rd ant 4th names and transfermarkt names does not contain these names,
# the join operator has to be built manually
dfWM22 = ws_tm_values.join(dfCompetition=dfWM22, dfValues=dfWMValues)

dataMarketValue = ws_tm_values.tTestMarketValue(df=dfWM22)

dfResult = pd.DataFrame(dataMarketValue)
 # save the dataframe in a json like format
dfResult.to_json("results/tTest_market_value_WM.json")
