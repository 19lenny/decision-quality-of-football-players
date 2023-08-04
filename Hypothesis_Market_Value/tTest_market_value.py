from typing import List
from scipy.stats import ttest_ind
import pandas as pd

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
t_Test = []
p_val = []
levene_test = []
p_val_levene = []
interpretation = []

"""
Der t-Test für unabhängige Gruppen setzt Varianzhomogenität voraus. 
Liegt Varianzheterogenität vor (also unterschiedliche Varianzen), so müssen unter anderem die Freiheitsgerade des t-Wertes angepasst werden. 
Ob die Varianzen homogen ("gleich") sind, lässt sich mit dem Levene-Test auf Varianzhomogenität prüfen. 
Der Levene-Test verwendet die Nullhypothese, dass sich die beiden Varianzen nicht unterscheiden. 
Daher bedeutet ein nicht signifikantes Ergebnis, dass sich die Varianzen nicht unterscheiden und somit Varianzhomogenität vorliegt. 
Ist der Test signifikant, so wird von Varianzheterogenität ausgegangen.
source: https://www.methodenberatung.uzh.ch/de/datenanalyse_spss/unterschiede/zentral/ttestunabh.html#3.4._Ergebnisse_des_t-Tests_f%C3%BCr_unabh%C3%A4ngige_Stichproben
https://www.statisticshowto.com/t-statistic/
"""

df_all = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
df_all = df_all.dropna(subset="xG_Delta_decision_alternative")

# check if the assumption of normal distribution is given
normal_dist = DataManipulation.check_normal_distribution(df_all)
if not normal_dist:
    normal_dist = DataManipulation.tranf_normal_distribution(df_all)


# H0: the decisions of players with a transfermarket value above mean are not better than decisions of players with a transfermarket value below mean.
# H1: the decisions of players with a transfermarket value above mean are better than decisions of players with a transfermarket value below mean.
# reject H0 if pval < alpha

#with median the groups are not the same size
mean_tm_val = df_all['value'].median()

# if the column score is bigger than 0 the team of the shooting player was currently winning, before the shot was fired
df_expensive = df_all.loc[df_all['value'] >= mean_tm_val]
mean_expensive = df_expensive['xG_Delta_decision_alternative'].mean()
xG_expensive = df_expensive['xG_Delta_decision_alternative'].values.tolist()
factor_one.append("player value above mean")
median_one.append(mean_expensive)
nr_shots_one.append(len(xG_expensive))

# if the score is smaller than 0 the team of the shooting player was currently loosing, before the shot was fired
df_cheap = df_all.loc[df_all['value'] < mean_tm_val]
mean_cheap = df_cheap['xG_Delta_decision_alternative'].mean()
xG_Delta_cheap = df_cheap['xG_Delta_decision_alternative'].values.tolist()
factor_two.append("player value below mean")
median_two.append(mean_cheap)
nr_shots_two.append(len(xG_Delta_cheap))

# add the interpretation for the current calculations
if mean_expensive > mean_cheap:
    interpretation.append("The decisions were in average " + str(mean_expensive - mean_cheap) + " better when a player with a market value above mean took the shot.")
else: interpretation.append("The decisions were in average " + str(mean_cheap - mean_expensive) + " better when a player with a market value below mean took the shot.")

lev, p = levene(xG_expensive, xG_Delta_cheap)
levene_test.append(lev)
p_val_levene.append(p)
result_winning_vs_loosing, pVal = ttest_ind(xG_expensive, xG_Delta_cheap)
t_Test.append(result_winning_vs_loosing)
p_val.append(pVal)

"""
"Je nach Fragestellung kann es interessant sein, die Differenz zwischen den beiden Variablen zusätzlich anzugeben. " \
"Sie steht in der Spalte Mittlere Differenz. " \
"Aus der Tabelle mit den deskriptiven Statistiken wissen wir, dass die Gruppe ohne Alkohol kürzere Reaktionszeiten hatten" \
" als die Gruppe mit. Wenn wir die Differenz berichten wollen, sollten wir noch ein Maß für die Variabilität dieser Differenz angeben," \
" da der Wert alleine betrachtet nur wenig aussagekräftig ist."

The greater the T, the more evidence you have that your team’s scores are significantly different from average. 
A smaller T value is evidence that your team’s score is not significantly different from average. 
The p-value tells you what the odds are that your results could have happened by chance.
https://www.statisticshowto.com/t-statistic/
"""
data = pd.DataFrame({"factor one" : factor_one,
                     "factor two" :factor_two,
                     "median one": median_one,
                     "median two": median_two,
                     "tTest" : t_Test,
                     "p_val" : p_val,
                     "interpretation" : interpretation,
                     "number of shots one": nr_shots_one,
                     "number of shots two": nr_shots_two,
                     "levene val": levene_test,
                     "p_val levene": p_val_levene})



data.to_json("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Hypothesis_Market_Value/results/tTest_market_value.json")