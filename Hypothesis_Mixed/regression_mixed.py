from SetUp import JSONtoDF, CONSTANTS
from Model import model_info
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

dfAll = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
df = dfAll

# prepare for period dummy
df = df.loc[(df["period"] == 1) | (df["period"] == 2)]
conditions = [
    (df['period'] == 1),
    (df['period'] == 2)
]
values = ["first_half_rt", "second_half_rt"]
df['period_string'] = np.select(conditions, values)
# prepare for scoring dummmy
conditions = [
(df['score'] == 1),
(df['score'] == 0),
(df['score'] == -1)
]
values = ["winning", "drawing", "loosing"]
df['score_string'] = np.select(conditions, values)

# prepare for is group stage dummy
df['is_group_stage'] = np.where(df['competition_stage'] == "Group Stage", 1, 0)

df = df[['period_string', "score_string", "is_group_stage", "value","xG_Delta_decision_alternative"]]

# perform the multiple linear regression with categorical variables using the formula API
model = smf.ols('xG_Delta_decision_alternative ~ C(period_string) + C(score_string) +C(is_group_stage) + value', data=df).fit()

# print the summary of the model
print(model.summary())

"""
The coefficient of the variable time_period for the category second_half is 15. 
This means that the predicted value of the dependent variable for the second half of the time period is higher than the first half by 15 units, 
while holding all other variables constant.
However, the coefficient for the first_half category is not reported in the summary output because it is used as the reference category. 
In other words, the effect of time_period on the dependent variable is estimated as the difference between the predicted values for second_half and first_half. 
So, we can't directly interpret the coefficient for first_half because it is absorbed into the intercept term.


The coefficients for the categorical variable score represent the difference in the predicted value of the dependent variable for the categories relative to the reference category, which in this case is likely winning.

If the coefficient for drawing is 3 and the coefficient for losing is 4, it means that, all else being equal, 
the predicted value of the dependent variable for the drawing category is 3 units higher than the predicted value
for the reference category (likely winning), and the predicted value for the losing category is 4 units higher
than the reference category.

If the coefficient for losing is 4 and the coefficient for drawing is 3, 
then all else being equal, the predicted value of the dependent variable for the losing category is expected to be higher
than the predicted value for the drawing category by 1 unit. This suggests that losing has a stronger positive association
with the dependent variable than drawing.

source: UCLA Institute for Digital Research and Education: Interpreting Regression Coefficients
"""