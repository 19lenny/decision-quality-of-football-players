from SetUp import JSONtoDF, CONSTANTS
from Model import model_info
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm

"""
Interpretation of summary:
In general, the regression coefficient on a dummy variable gives us the average increase in $y_{i}$ observed
 when the dummy is equal to 1 (with respect to the base case in which the dummy is equal to 0).
In our case the dummy variable is 1, when the shot is taken in the first half. 
Ergo if the dummy variable is positive the y value is increasing. 
An increasing y value (=xG_Delta_decision_alternative) means that the player makes better decisions in comparison to its best alternative.
if the dummy variable is negative, it means the xG_Delta_decision_alternative increases (=the decisions are getting better) in the second half.
source: https://www.statlect.com/fundamentals-of-statistics/dummy-variable

if there are only two possibilites, we only need k-1 values:
Notice that we have added only one dummy variable period_string_first_half and not both,
period_string_first_half and period_string_second_half.
We did this to avoid perfect collinearity as every xG_Delta_decision_alternative in the data set is either created in first or second half.
There is no third type. 
In this case, regression intercept captures the effect of period_string_first_half. 
Specifically, the estimated value of the regression intercept in the trained model is the estimated mean value of all xG Delta Decisions.
Alternately, we could have added both period_string_first_half and period_string_second_half and left out the regression intercept. 
In this later case, because the model would not have the regression intercept, we would not be able to use the R-squared value to judge its goodness-of-fit.
"""

df_all = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)

def regression_time(period1, period2, name_period1, name_period2):
    # only split in to the periods wished
    #todo: this must be done in orchestrator
    df = df_all.loc[(df_all["period"] == period1) | (df_all["period"] == period2)]
    conditions = [
        (df['period'] == period1),
        (df['period'] == period2)
    ]
    values = [name_period1, name_period2]
    df['period_string'] = np.select(conditions, values)
    df_with_dummies = pd.get_dummies(data=df, columns=['period_string'])
    #only take the first period. The reasoning for this is in the description of this file
    name = 'period_string_'+ name_period1
    reg_exp = 'xG_Delta_decision_alternative ~ '+name
    olsr_model = smf.ols(formula=reg_exp, data=df_with_dummies)
    olsr_model_results = olsr_model.fit()
    """
    SOURCE: https://timeseriesreasoning.com/contents/dummy-variables-in-a-regression-model/
    adj. R2: How much the time variable / period variable is able to explain the variance in the xG Delta Decision.
    The adj. R2 is not the most important value, since we don't expect to explain the variance only with time. 
    Prob F-statistic: if this is significant (< alpha), than it says the model can predict the data better than a mean model, 
    which is a flat horizontal line passing through the mean value of xG_Delta_decision_alternative.
    P>|t|: checks if the coefficients of our model are significant.
    Intercept: the intercept is the mean of the 'xG_Delta_decision_alternative' column.
    Coefficient period_string_first_half: If it is positive, than it means, Player that shot in the first half have taken a better decision by the coefficient value.
    If it is negative, than it means, Player that shot in the first half have taken a worse decision by the coefficient parameter.
    Coefficient period_string_second_half: Coefficient period_string_first_half*(-1)
    """
    model_info.show_info(olsr_model_results)
    return olsr_model_results

#1st half vs 2nd half
print("-----------------------------THIS IS THE RESULT FOR FIRST HALF VS SECOND HALF------------------------------------")
result = regression_time(period1=1, period2=2, name_period1="first_half", name_period2="second_half")
with open('G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Hypothesis_Time/results/regression_time.txt', 'w') as fh:
    fh.write(result.summary().as_text())
"""print("-----------------------------THIS IS THE RESULT FOR FIRST HALF OT VS SECOND HALF OT------------------------------------")
#1st half ot vs 2nd half ot
result2 = regression_time(period1=3, period2=4, name_period1="first_half_ot", name_period2="second_half_ot")
"""

