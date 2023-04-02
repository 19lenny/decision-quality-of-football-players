# import all shots EM2020
from SetUp import JSONtoDF, CONSTANTS, TM_values
import pandas as pd

# all competitions

#dfEMValues = ws_tm_values.transfermarketValue("EM")
#dfEMValues.to_json("ValuesEM.json")
dfEM20 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONEM2020)
dfEMValues = JSONtoDF.createDF("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Hypothesis_Market_Value/ValuesEM.json")
# since the statsbomb names contains 3rd ant 4th names and transfermarkt names does not contain these names,
# the join operator has to be built manually
dfEM20 = ws_tm_values.join(dfCompetition=dfEM20, dfValues=dfEMValues)

# dfWMValues = ws_tm_values.transfermarketValue("WM")
# dfWMValues.to_json("ValuesWM.json")
dfWM22 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONWM2022)
dfWMValues = JSONtoDF.createDF("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Hypothesis_Market_Value/ValuesWM.json")
# since the statsbomb names contains 3rd ant 4th names and transfermarkt names does not contain these names,
# the join operator has to be built manually
dfWM22 = ws_tm_values.join(dfCompetition=dfWM22, dfValues=dfWMValues)

dfTogether = pd.concat([dfWM22, dfEM20])
dataMarketValue = ws_tm_values.tTestMarketValue(df=dfTogether)
dfResultComp = pd.DataFrame(dataMarketValue)
 # save the dataframe in a json like format
dfResultComp.to_json("results/tTest_market_value_competitions.json")

# EM

dataMarketValue = ws_tm_values.tTestMarketValue(df=dfEM20)
dfResultEM = pd.DataFrame(dataMarketValue)
 # save the dataframe in a json like format
dfResultEM.to_json("results/tTest_market_value_EM.json")

#WM

dataMarketValue = ws_tm_values.tTestMarketValue(df=dfWM22)
dfResultWM = pd.DataFrame(dataMarketValue)
 # save the dataframe in a json like format
dfResultWM.to_json("results/tTest_market_value_WM.json")


