from typing import List
from scipy.stats import ttest_ind
import pandas as pd

from SetUp import JSONtoDF, CONSTANTS
from scipy.stats import levene
"""
this file tests the time hypotheses based on tTests.
the results are saved in a json format.
"""
# set up
first_half = 1
second_half = 2
first_half_ot = 3
second_half_ot = 4
factor_one = []
factor_two = []
median_one = []
median_two = []
nr_shots_one = []
nr_shots_two = []
t_Test = []
p_val = []
levene_test = []
p_val_levene = []

"""
Der t-Test für unabhängige Gruppen setzt Varianzhomogenität voraus. 
Liegt Varianzheterogenität vor (also unterschiedliche Varianzen), so müssen unter anderem die Freiheitsgerade des t-Wertes angepasst werden. 
Ob die Varianzen homogen ("gleich") sind, lässt sich mit dem Levene-Test auf Varianzhomogenität prüfen. 
Der Levene-Test verwendet die Nullhypothese, dass sich die beiden Varianzen nicht unterscheiden. 
Daher bedeutet ein nicht signifikantes Ergebnis, dass sich die Varianzen nicht unterscheiden und somit Varianzhomogenität vorliegt. 
Ist der Test signifikant, so wird von Varianzheterogenität ausgegangen.
source: https://www.methodenberatung.uzh.ch/de/datenanalyse_spss/unterschiede/zentral/ttestunabh.html#3.4._Ergebnisse_des_t-Tests_f%C3%BCr_unabh%C3%A4ngige_Stichproben
"""
#todo: levene test correct, ttest correct?

# H0: the decisions in the first half are the same as the ones in the second half
# H1: first half decisions are better than second half ones
# reject H0 if pval < alpha
df_first_half = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
df_first_half = df_first_half.loc[df_first_half['period'] == first_half]
mean_first_half = df_first_half['xG_Delta_decision_alternative'].mean()
xG_Delta_first_half = df_first_half['xG_Delta_decision_alternative'].values.tolist()
factor_one.append("first half regular time")
median_one.append(mean_first_half)
nr_shots_one.append(len(xG_Delta_first_half))

df_second_half = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
df_second_half = df_second_half.loc[df_second_half['period'] == second_half]
mean_second_half = df_second_half['xG_Delta_decision_alternative'].mean()
xG_Delta_second_half = df_second_half['xG_Delta_decision_alternative'].values.tolist()
factor_two.append("second half regular time")
median_two.append(mean_second_half)
nr_shots_two.append(len(xG_Delta_second_half))

lev, p = levene(xG_Delta_first_half, xG_Delta_second_half)
levene_test.append(lev)
p_val_levene.append(p)
result_first_vs_second, pVal = ttest_ind(xG_Delta_first_half, xG_Delta_second_half)
t_Test.append(result_first_vs_second)
p_val.append(pVal)


# H0: the decisions in the first half of the overtime are the same as the ones in the second half of the overtime
# H1: first half of overtime decisions are better than second half overtime ones
# reject H0 if pval < alpha
df_first_half_ot = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
df_first_half_ot = df_first_half_ot.loc[df_first_half_ot['period'] == first_half_ot]
mean_first_half_ot = df_first_half_ot['xG_Delta_decision_alternative'].mean()
xG_Delta_first_half_ot = df_first_half_ot['xG_Delta_decision_alternative'].values.tolist()
factor_one.append("first half over time")
median_one.append(mean_first_half_ot)
nr_shots_one.append(len(xG_Delta_first_half_ot))

df_second_half_ot = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
df_second_half_ot = df_second_half_ot.loc[df_second_half_ot['period'] == second_half_ot]
mean_second_half_ot = df_second_half_ot['xG_Delta_decision_alternative'].mean()
xG_Delta_second_half_ot = df_second_half_ot['xG_Delta_decision_alternative'].values.tolist()
factor_two.append("second half over time")
median_two.append(mean_second_half_ot)
nr_shots_two.append(len(xG_Delta_second_half_ot))

lev, p = levene(xG_Delta_first_half_ot, xG_Delta_second_half_ot)
levene_test.append(lev)
p_val_levene.append(p)
result_first_vs_second_ot, pVal = ttest_ind(xG_Delta_first_half_ot, xG_Delta_second_half_ot)
t_Test.append(result_first_vs_second_ot)
p_val.append(pVal)

# todo: unterschied in den Gruppen wahrscheinlich zu gross
# H0: the decisions in the regular time are the same as the ones in the overtime
# H1: regular time decisions are better than overtime decisions
# reject H0 if pval < alpha
df_regular_time = pd.concat([df_first_half, df_second_half])
mean_regular_time = df_regular_time['xG_Delta_decision_alternative'].mean()
xG_Delta_regular_time = df_regular_time['xG_Delta_decision_alternative'].values.tolist()
factor_one.append("regular time")
median_one.append(mean_regular_time)
nr_shots_one.append(len(xG_Delta_regular_time))

df_over_time = pd.concat([df_first_half_ot, df_second_half_ot])
mean_over_time = df_over_time['xG_Delta_decision_alternative'].mean()
xG_Delta_over_time = df_over_time['xG_Delta_decision_alternative'].values.tolist()
factor_two.append("over time")
median_two.append(mean_over_time)
nr_shots_two.append(len(xG_Delta_over_time))

lev, p = levene(xG_Delta_first_half_ot, xG_Delta_second_half_ot)
levene_test.append(lev)
p_val_levene.append(p)
result_regular_vs_over, pVal = ttest_ind(xG_Delta_regular_time, xG_Delta_over_time)
t_Test.append(result_regular_vs_over)
p_val.append(pVal)


# todo: add interpretation
data = pd.DataFrame({"factor one" : factor_one,
                     "factor two" :factor_two,
                     "median one": median_one,
                     "median two": median_two,
                     "tTest" : t_Test,
                     "p_val" : pVal,
                     "number of shots one": nr_shots_one,
                     "number of shots two": nr_shots_two,
                     "levene val": levene_test,
                     "p_val levene": p_val_levene})


data.to_json("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Hypothesis_Time/results/tTest_time.json")