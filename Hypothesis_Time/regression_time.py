from SetUp import JSONtoDF, CONSTANTS
from Model import model_info
import numpy as np
import statsmodels.formula.api as smf

"""
Interpretation of summary:
In general, the regression coefficient on a dummy variable gives us the average increase in $y_{i}$ observed
 when the dummy is equal to 1 (with respect to the base case in which the dummy is equal to 0).
In our case the dummy variable is 1, when the shot is taken in the first half. 
Ergo if the dummy variable is positive the y value is increasing. 
An increasing y value (=xG_Delta_decision_alternative) means that the player makes better decisions in comparison to its best alternative.
if the dummy variable is negative, it means the xG_Delta_decision_alternative increases (=the decisions are getting better) in the second half.
source: https://www.statlect.com/fundamentals-of-statistics/dummy-variable
"""

df_all = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)

def regression_time(period1, period2):
    # only split in to the periods wished

    df = df_all.loc[(df_all["period"] == period1) | (df_all["period"] == period2)]
    # https://medium.com/analytics-vidhya/implementing-linear-regression-using-sklearn-76264a3c073c
    # https://www.geeksforgeeks.org/how-to-get-regression-model-summary-from-scikit-learn/
    df['is_first_period'] = np.where(df['period'] == period1, 1, 0)
    df = df[['xG_Delta_decision_alternative', 'is_first_period']]
    model = smf.ols(formula='xG_Delta_decision_alternative ~ is_first_period',
                    data=df).fit()
    # model summary
    model_info.show_info(model)
    return model

#1st half vs 2nd half
result = regression_time(period1=1, period2=2)
print("-----------------------------NEXT------------------------------------")
#1st half ot vs 2nd half ot
result2 = regression_time(period1=3, period2=4)

with open('G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Hypothesis_Time/results/regresstion_time.txt', 'w') as fh:
    fh.write(result.summary().as_text())