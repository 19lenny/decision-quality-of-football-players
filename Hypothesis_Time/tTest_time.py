from typing import List
from scipy.stats import ttest_ind
import pandas as pd
import tTestExecution
from SetUp import JSONtoDF, CONSTANTS

# H0: the decision in the first x minutes to the last 90-x minutes have no difference
# reject H0 if pval < alpha
first_half = 1
second_half = 2
first_half_overtime = 3
second_half_overtime = 4

# tTest evaluation regular time

dfEM20 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONEM2020)
dfEM20Results = tTestExecution.tTestTime(df=dfEM20, start_period=first_half,end_period=second_half)
# save the dataframe in a json like format
dfEM20Results.to_json("results/tTest_regulartime_EM20.json")
dfWM22 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONWM2022)
dfWM22Results = tTestExecution.tTestTime(df=dfWM22, start_period=first_half,end_period=second_half)
dfWM22Results.to_json("results/tTest_regulartime_WM22.json")
dfShotEval = pd.concat([dfEM20, dfWM22])
dfCompetitionResults = tTestExecution.tTestTime(df=dfShotEval, start_period=first_half,end_period=second_half)
dfCompetitionResults.to_json("results/tTest_regulartime_all_comp.json")

# tTest evaluation over time

dfEM20ResultsOT = tTestExecution.tTestTime(df=dfEM20, start_period=first_half_overtime,end_period=second_half_overtime)
# save the dataframe in a json like format
dfEM20ResultsOT.to_json("results/tTest_overtime_EM20.json")

dfWM22ResultsOT = tTestExecution.tTestTime(df=dfWM22, start_period=first_half_overtime,end_period=second_half_overtime)
dfWM22ResultsOT.to_json("results/tTest_overtime_WM22.json")

dfCompetitionResultsOT = tTestExecution.tTestTime(df=dfShotEval, start_period=first_half_overtime,end_period=second_half_overtime)
dfCompetitionResultsOT.to_json("results/tTest_overtime_all_comp.json")


# regular time vs. overtime
dfEM20RvOT = tTestExecution.tTestRegularvsOT(df=dfEM20, end_period_regular=second_half, start_period_OT=first_half_overtime )
dfEM20RvOT.to_json("results/tTest_regVSovertime_EM20.json")

dfWM22RvOT = tTestExecution.tTestRegularvsOT(df=dfWM22, end_period_regular=second_half, start_period_OT=first_half_overtime)
dfWM22RvOT.to_json("results/tTest_regVSovertime_WM22.json")

dfCompetitionResultsRvsOT = tTestExecution.tTestRegularvsOT(df=dfShotEval, end_period_regular=second_half, start_period_OT=first_half_overtime)
dfCompetitionResultsRvsOT.to_json("results/tTest_regVSovertime_all_comp.json")