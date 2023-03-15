# import all shots EM2020
from typing import List
import re
from SetUp import JSONtoDF, CONSTANTS
import pandas as pd
import ws_tm_values
from scipy.stats import ttest_ind
import ws_tm_values
from difflib import SequenceMatcher

#dfEMValues = ws_tm_values.transfermarketValue("EM")
#dfEMValues.to_json("ValuesEM.json")
dfEM20 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONEM2020)
dfEMValues = JSONtoDF.createDF("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Hypothesis_market_value/ValuesEM.json")

# since the statsbomb names contains 3rd ant 4th names and transfermarkt names does not contain these names,
# the join operator has to be built manually
dfEM20 = ws_tm_values.join(dfCompetition=dfEM20, dfValues=dfEMValues)

dataMarketValue = ws_tm_values.tTestMarketValue(df=dfEM20)

dfResult = pd.DataFrame(dataMarketValue)
 # save the dataframe in a json like format
dfResult.to_json("results/tTest_market_value_EM.json")
