from typing import List
from scipy.stats import ttest_ind
import pandas as pd
import scipy.stats as stats
from SetUp import JSONtoDF, CONSTANTS, DataManipulation
from scipy.stats import levene
"""
this file tests the time hypotheses based on tTests.
the results are saved in a json format.
"""

factor_one = []
factor_two = []
median_one = []
median_two = []
nr_shots_one = []
nr_shots_two = []
u_Test = []
p_val = []
interpretation = []



df_all = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
df_all = df_all.loc[df_all['score'] != 0]

# check if the assumption of normal distribution is given
normal_dist = DataManipulation.check_normal_distribution(df_all)
if not normal_dist:
    normal_dist = DataManipulation.tranf_normal_distribution(df_all)


# H0: the decisions when winning are equal to the decisions when loosing
# H1: the decisions when winning are not equal to the decisions when loosing
# reject H0 if pval < alpha

# if the column score is bigger than 0 the team of the shooting player was currently winning, before the shot was fired
df_winning = df_all.loc[df_all['score'] > 0]
mean_winning = df_winning['xG_Delta_decision_alternative'].mean()
xG_Delta_winning = df_winning['xG_Delta_decision_alternative'].values.tolist()
factor_one.append("teams winning")
median_one.append(mean_winning)
nr_shots_one.append(len(xG_Delta_winning))

# if the score is smaller than 0 the team of the shooting player was currently loosing, before the shot was fired
df_loosing = df_all.loc[df_all['score'] < 0]
mean_loosing = df_loosing['xG_Delta_decision_alternative'].mean()
xG_Delta_loosing = df_loosing['xG_Delta_decision_alternative'].values.tolist()
factor_two.append("teams loosing")
median_two.append(mean_loosing)
nr_shots_two.append(len(xG_Delta_loosing))

# add the interpretation for the current calculations
if mean_winning > mean_loosing:
    interpretation.append("The decisions were in average " + str(mean_winning - mean_loosing) + " better when winning than when loosing.")
else: interpretation.append("The decisions were in average " + str(mean_loosing - mean_winning) + " better when loosing than when winning.")


result_winning_vs_loosing, pVal = stats.mannwhitneyu(xG_Delta_winning, xG_Delta_loosing, alternative='two-sided')
u_Test.append(result_winning_vs_loosing)
p_val.append(pVal)


data = pd.DataFrame({"factor one" : factor_one,
                     "factor two" :factor_two,
                     "median one": median_one,
                     "median two": median_two,
                     "uTest" : u_Test,
                     "p_val" : p_val,
                     "interpretation" : interpretation,
                     "number of shots one": nr_shots_one,
                     "number of shots two": nr_shots_two})



data.to_json("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Hypothesis_Score/results/uTest_score.json")