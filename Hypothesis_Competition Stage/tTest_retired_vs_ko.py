from scipy.stats import ttest_ind

from SetUp import JSONtoDF, CONSTANTS
import prepareDataframeStage
import pandas as pd

# H0 the teams that had to leave after the group stage make the same decisions
# as the teams that were going through the knock out phase

# first add WM 22 and EM 20 to one dataframe together
dfEM20 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONEM2020)

teams_ko_em20 = prepareDataframeStage.TeamsInStage(dfEM20, "Round of 16")

df_KO_teams_em20 = dfEM20[dfEM20['team'].isin(teams_ko_em20)]
df_group_teams_em20 = dfEM20[~dfEM20['team'].isin(teams_ko_em20)]


dfWM22 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONWM2022)

teams_ko_wm22 = prepareDataframeStage.TeamsInStage(dfWM22, "Round of 16")

df_KO_teams_wm22 = dfWM22[dfWM22['team'].isin(teams_ko_wm22)]
df_group_teams_wm22 = dfWM22[~dfWM22['team'].isin(teams_ko_wm22)]
# this can only be contacted here, since teams were in the playoffs in 20 but not achieved playofss in 22,
# example denmark
df_KO_all = pd.concat([df_KO_teams_em20, df_KO_teams_wm22])
df_group_all = pd.concat([df_group_teams_em20, df_group_teams_wm22])
KO_all = df_KO_all['xG_Delta_decision_alternative'].values.tolist()
group_all = df_group_all['xG_Delta_decision_alternative'].values.tolist()

t_stat, p_value = ttest_ind(group_all, KO_all)