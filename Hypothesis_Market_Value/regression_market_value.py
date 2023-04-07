from SetUp import JSONtoDF, CONSTANTS
from Model import model_info

import statsmodels.formula.api as smf


df_all = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)

reg_exp = 'xG_Delta_decision_alternative ~ value'
olsr_model = smf.ols(formula=reg_exp, data=df_all)
olsr_model_results = olsr_model.fit()
print(model_info.show_info(olsr_model_results))
with open('G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Hypothesis_Market_Value/results/regression_value.txt', 'w') as fh:
    fh.write(olsr_model_results.summary().as_text())


