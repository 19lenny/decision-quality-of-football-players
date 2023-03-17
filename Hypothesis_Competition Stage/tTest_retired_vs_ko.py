from typing import List

from scipy.stats import ttest_ind

from SetUp import JSONtoDF, CONSTANTS
import prepareDataframeStage
import pandas as pd

t_stat: List[float] = [0.0] * 3
p_values: List[float] = [0.0] * 3

# H0 the teams that had to leave after the group stage make the same decisions
# as the teams that were going through the knock out phase

# first add WM 22 and EM 20 to one dataframe together
dfEM20 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONEM2020)

teams_ko_em20 = prepareDataframeStage.TeamsInStage(dfEM20, "Round of 16")
# all teams that made it to the knock out round
df_KO_teams_em20 = dfEM20[dfEM20['team'].isin(teams_ko_em20)]
# all teams that have not achieved the knock out round
df_group_teams_em20 = dfEM20[~dfEM20['team'].isin(teams_ko_em20)]

t_stat[0], p_values[0] = ttest_ind(df_group_teams_em20['xG_Delta_decision_alternative'].values.tolist(), df_KO_teams_em20['xG_Delta_decision_alternative'].values.tolist())


dfWM22 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONWM2022)

teams_ko_wm22 = prepareDataframeStage.TeamsInStage(dfWM22, "Round of 16")

df_KO_teams_wm22 = dfWM22[dfWM22['team'].isin(teams_ko_wm22)]
df_group_teams_wm22 = dfWM22[~dfWM22['team'].isin(teams_ko_wm22)]

t_stat[1], p_values[1] = ttest_ind(df_group_teams_wm22['xG_Delta_decision_alternative'].values.tolist(), df_KO_teams_wm22['xG_Delta_decision_alternative'].values.tolist())

# this can only be contacted here, since teams were in the playoffs in 20 but not achieved playoffs in 22,
# example denmark
df_KO_all = pd.concat([df_KO_teams_em20, df_KO_teams_wm22])
df_group_all = pd.concat([df_group_teams_em20, df_group_teams_wm22])


t_stat[2], p_values[2] = ttest_ind(df_group_all['xG_Delta_decision_alternative'].values.tolist(), df_KO_all['xG_Delta_decision_alternative'].values.tolist())
# all arrays must be same length
comp = ["EM", "WM", "both"]
data = {'competition': comp,
        'T-stat': t_stat,
        'P-Val': p_values
}
dfResults = pd.DataFrame(data)
dfResults.to_json("results/tTest_retired_vs_KO_all_competitions.json")