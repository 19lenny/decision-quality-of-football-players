from SetUp import JSONtoDF, CONSTANTS
from Model import model_info
import numpy as np
import statsmodels.api as sm
import pandas as pd
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

#https://timeseriesreasoning.com/contents/dummy-variables-in-a-regression-model/
conditions = [
(df_all['score'] == 1),
(df_all['score'] == 0),
(df_all['score'] == -1)
]
values = ["winning", "drawing", "loosing"]
df_all['score_string'] = np.select(conditions, values)
df_with_dummies = pd.get_dummies(data=df_all, columns=['score_string'])
# Next, we’ll construct the regression equation in Patsy syntax:
# We’ll leave out one dummy variable (score_string_drawing) to void perfect collinearity.
# The regression model’s intercept will hold the coefficient of score_string_drawing.

reg_exp = 'xG_Delta_decision_alternative ~ score_string_winning + score_string_loosing'
olsr_model = smf.ols(formula=reg_exp, data=df_with_dummies)
olsr_model_results = olsr_model.fit()
print(olsr_model_results.summary())
with open('G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Hypothesis_Score/results/regression_score.txt', 'w') as fh:
    fh.write(olsr_model_results.summary().as_text())
"""
SOURCE: https://timeseriesreasoning.com/contents/dummy-variables-in-a-regression-model/
adj. R2: How much the time variable / period variable is able to explain the variance in the xG Delta Decision.
The adj. R2 is not the most important value, since we don't expect to explain the variance only with time. 
Prob F-statistic: This variable is very important. 
If it is significant (< alpha), than it says the model can predict the data better than a mean model, 
which is a flat horizontal line passing through the mean value of xG_Delta_decision_alternative.
P>|t|: checks if the coefficients of our model are significant.
Intercept: the intercept is the estimated mean of xG_Delta_decision_alternative based on score_string_drawing, since we left this one out in the model.
Coefficients: The coefficients of the two specific dummies for winning and loosing represent the extent to which the mean of the corresponding style deviates
 from the estimated mean xG_Delta_decision_alternative of drawing.
 If a coefficient is not significant the estimated xG_Delta_decision_alternative is the same when drawing or winning and winning would have no ability to explain any of the variance in the xG_Delta_decision_alternative.
Coefficient winning: If it is positive, than it means, Player that shoot while winning have a better decision than while drawing
If it is negative, than it means, Player that shoot while winning have a worse decision than while drawing
Coefficient loosing: If it is positive, than it means, Player that shoot while loosing have a better decision than while drawing
If it is negative, than it means, Player that shoot while loosing have a worse decision than while drawing
*IF coefficient winning > loosing --> the decision made while winning is better while when loosing.*

"""

