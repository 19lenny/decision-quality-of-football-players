from scipy.stats import ttest_ind
import pandas as pd

from SetUp import JSONtoDF, CONSTANTS, DataManipulation
from scipy.stats import levene

def keep_KO_Teams(df):
    # create a dataframe with all teams that achieved the round of 16
    # this searches for the teams and drops all duplicates, since a team cannot achieve multiple time
    KO_stage = df[["home_team", "away_team"]][df['competition_stage'] == "Round of 16"].drop_duplicates()
    KO_stage = pd.concat([KO_stage['home_team'], KO_stage['away_team'].rename({'away_team': 'home_team'})])
    KO_stage = KO_stage.values.tolist()
    # keep only shots of teams that are in list of the round of 16
    dfManipulated = df[df['team'].isin(KO_stage)]
    dfManipulated.reset_index(drop=True, inplace=True)
    return dfManipulated

def preparation(df):
    # create a separate dataframe for all competitions since a team could have processed to the next round in one competition but not in others, example denmark

    # dfEM2020
    dfEM = df.loc[(df['competition'] == "Europe - UEFA Euro") & (df['season'] == 2020)]
    dfEM = keep_KO_Teams(dfEM)
    dfEM.reset_index(drop=True, inplace=True)

    # dfWM18
    dfWM18 = df.loc[(df['competition'] == "International - FIFA World Cup") & (df['season'] == 2018)]
    dfWM18 = keep_KO_Teams(dfWM18)
    dfWM18.reset_index(drop=True, inplace=True)

    # dfWM22
    dfWM22 = df.loc[(df['competition'] == "International - FIFA World Cup") & (df['season'] == 2022)]
    dfWM22 = keep_KO_Teams(dfWM22)
    dfWM22.reset_index(drop=True, inplace=True)

    dfAllMatches = pd.concat([dfEM, dfWM18, dfWM22])
    return dfAllMatches


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
# prepare df that only teams that played in the knock out appear also in the group stage
df = preparation(df=JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS))

# check if the assumption of normal distribution is given
normal_dist = DataManipulation.check_normal_distribution(df)
if not normal_dist:
    normal_dist = DataManipulation.tranf_normal_distribution(df)


# H0: the decisions when in knock out stage are equal as in group stage
# H1: the decisions when in knock out stage are not equal as in group stage
# reject H0 if pval < alpha

#2 groups:
# group 1 --> teams that achieved the knock out stage. These are their decisions in the knock out phase.
ko_stages = ["Round of 16", "Quarter-finals", "Semi-finals", "Final"]
dfAllMatches_Knock_Out_Stage = df.loc[df['competition_stage'].isin(ko_stages)]

mean_KO = dfAllMatches_Knock_Out_Stage['xG_Delta_decision_alternative'].mean()
xG_Delta_KO = dfAllMatches_Knock_Out_Stage['xG_Delta_decision_alternative'].values.tolist()
factor_one.append("decisions made in knock out stage")
median_one.append(mean_KO)
nr_shots_one.append(len(xG_Delta_KO))


# group 2 --> teams that achieved the knock out stage. These are their decisions in the group phase.
dfAllMatches_Group_Stage = df.loc[df['competition_stage'] == "Group Stage"]
mean_GP = dfAllMatches_Group_Stage['xG_Delta_decision_alternative'].mean()
xG_Delta_GP = dfAllMatches_Group_Stage['xG_Delta_decision_alternative'].values.tolist()
factor_two.append("decisions made in group stage")
median_two.append(mean_GP)
nr_shots_two.append(len(xG_Delta_GP))


# add the interpretation for the current calculations
if mean_KO > mean_GP:
    interpretation.append("The decisions were in average " + str(mean_KO - mean_GP) + " better when the players shot was during knock out phase.")
else: interpretation.append("The decisions were in average " + str(mean_GP - mean_KO) + " better when the players shot was during group stage.")

lev, p = levene(xG_Delta_KO, xG_Delta_GP)
levene_test.append(lev)
p_val_levene.append(p)
result_KO_vs_GP, pVal = ttest_ind(xG_Delta_KO, xG_Delta_GP)
t_Test.append(result_KO_vs_GP)
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

data.to_json("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Hypothesis_Competition Stage/results/tTest_competition_stage.json")



