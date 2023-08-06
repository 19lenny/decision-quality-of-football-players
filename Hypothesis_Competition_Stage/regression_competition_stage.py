from SetUp import JSONtoDF, CONSTANTS
from Model import model_info
import numpy as np
import statsmodels.api as sm
import pandas as pd
import statsmodels.formula.api as smf
import tTest_competition_stage


# prepare df that only teams that played in the knock out appear also in the group stage
df = tTest_competition_stage.preparation(df=JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS))
df_with_dummies = df
df_with_dummies['is_group_stage'] = np.where(df['competition_stage'] == "Group Stage", 1, 0)
reg_exp = 'xG_Delta_decision_alternative ~ is_group_stage'
olsr_model = smf.ols(formula=reg_exp, data=df_with_dummies)
olsr_model_results = olsr_model.fit()
model_info.show_info(olsr_model_results)
with open('/Hypothesis_Competition_Stage/results/regression_competition_stage.txt', 'w') as fh:
    fh.write(olsr_model_results.summary().as_text())
"""
SOURCE: https://timeseriesreasoning.com/contents/dummy-variables-in-a-regression-model/
adj. R2: How much the competition stage variable is able to explain the variance in the xG Delta Decision.
The adj. R2 is not the most important value, since we don't expect to explain the variance only with time. 
Prob F-statistic: if this is significant (< alpha), than it says the model can predict the data better than a mean model, 
which is a flat horizontal line passing through the mean value of xG_Delta_decision_alternative.
P>|t|: checks if the coefficients of our model are significant.
Intercept: the intercept is the mean of the 'xG_Delta_decision_alternative' column.
Coefficient is_group_stage: If it is positive, than it means, Players that shot during the group stage have taken a better decision by the coefficient value.
If it is negative, than it means, Players that shot during the group stage have taken a worse decision by the coefficient parameter.
Coefficient is_KO_stage: Coefficient is_group_stage*(-1)
"""

