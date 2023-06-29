from SetUp import JSONtoDF, CONSTANTS, DataManipulation
import DataManipulation_competition_stage as dmcs
import scipy.stats as stats
import pandas as pd
import numpy as np

# prepare df that only teams that played in the knock out appear also in the group stage
df = dmcs.preparation(df=JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS))
#drop all shots from the small final. it is not considered as a normal KO game and is therefore thrown out
df = df[df.competition_stage != "3rd Place Final"]
df = df.dropna(subset="xG_Delta_decision_alternative")
df.reset_index(drop=True, inplace=True)
ko_stages = ["Round of 16", "Quarter-finals", "Semi-finals", "Final"]

#csv for spss
df_csv = df
df_csv['group_KO'] = np.where(df['competition_stage'].isin(ko_stages), 1, 0)
#1 is in KO stage, 0 shot is not given in KO stage
df_csv.to_csv("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/SPSS/Hypothese Competition stage/dfCompetitionStage.csv")
df_all_desc = df_csv.describe()

factor_one = []
factor_two = []
median_one = []
median_two = []
nr_shots_one = []
nr_shots_two = []
u_Test = []
p_val = []
interpretation = []

#2 groups:
# group 1 --> teams that achieved the knock out stage. These are their decisions in the knock out phase.

dfAllMatches_Knock_Out_Stage = df.loc[df['competition_stage'].isin(ko_stages)]

Knock_Out_Stage_describe = dfAllMatches_Knock_Out_Stage.describe()

mean_KO = dfAllMatches_Knock_Out_Stage['xG_Delta_decision_alternative'].mean()
xG_Delta_KO = dfAllMatches_Knock_Out_Stage['xG_Delta_decision_alternative'].values.tolist()
factor_one.append("decisions made in knock out stage")
median_one.append(mean_KO)
nr_shots_one.append(len(xG_Delta_KO))


# group 2 --> teams that achieved the knock out stage. These are their decisions in the group phase.
dfAllMatches_Group_Stage = df.loc[df['competition_stage'] == "Group Stage"]
Group_Stage_describe = dfAllMatches_Group_Stage.describe()



mean_GP = dfAllMatches_Group_Stage['xG_Delta_decision_alternative'].mean()
xG_Delta_GP = dfAllMatches_Group_Stage['xG_Delta_decision_alternative'].values.tolist()
factor_two.append("decisions made in group stage")
median_two.append(mean_GP)
nr_shots_two.append(len(xG_Delta_GP))


if mean_KO > mean_GP:
    interpretation.append("The decisions were in average " + str(mean_KO - mean_GP) + " better when the players shot was during knock out phase.")
else: interpretation.append("The decisions were in average " + str(mean_GP - mean_KO) + " better when the players shot was during group stage.")

#two sided test, since we dont know which site should be better
result_KO_vs_GP, pVal = stats.mannwhitneyu(xG_Delta_KO, xG_Delta_GP, alternative = 'two-sided')
u_Test.append(result_KO_vs_GP)
p_val.append(pVal)

data = pd.DataFrame({"factor one" : factor_one,
                     "factor two" :factor_two,
                     "median one": median_one,
                     "median two": median_two,
                     "u_Test" : u_Test,
                     "p_val" : p_val,
                     "interpretation" : interpretation,
                     "number of shots one": nr_shots_one,
                     "number of shots two": nr_shots_two,})

data.to_json("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Hypothesis_Competition Stage/results/uTest_competition_stage.json")
