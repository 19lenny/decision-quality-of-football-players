from typing import List

from SetUp import JSONtoDF, CONSTANTS
from Model import model_info
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


def data_prep_teamnumber(df):
    # all teams that competed over time
    teams = df[["home_team", "away_team"]][df['competition_stage'] == "Group Stage"]
    teams = pd.concat([teams['home_team'], teams['away_team'].rename({'away_team': 'home_team'})])
    teams = teams.drop_duplicates()
    teams.reset_index(drop=True, inplace=True)
    teams = teams.values.tolist()
    #sort teams alphabetically
    teams = sorted(teams)

    # add the teams to a dictionary
    # every team has now a unique value
    teams_dict = {}
    x = 0
    for team in teams:
        teams_dict[team] = x
        x += 1

    # now manipulate the dataframe, such that every shot gets a number
    team_number: List[float] = [0.0] * len(df)
    for shot in range(len(df)):
        # what is the current team
        current_team = df['team'][shot]
        # what is the value for this team
        value = teams_dict[current_team]
        # add the value to the list that in the end is added to the complete df
        team_number[shot] = value

    # add the list to the df

    df['team_number'] = team_number
    print(teams_dict)
    return df
df_all = data_prep_teamnumber(JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS))
#save the df to csv, so it can be analyzed in SPSS
df_all.to_csv("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/SPSS/Robustness Check/dfTest_Teamnumbers.csv")
# perform the multiple linear regression with categorical variables using the formula API
model = smf.ols('xG_Delta_decision_alternative ~ C(team_number)', data=df_all).fit()
# print the summary of the model
print(model.summary())

#prepare for anova test, make groups
df_competition = data_prep_teamnumber(pd.read_csv("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/SPSS/Hypothese Competition stage/dfCompetitionStage.csv"))
#df_competition= df_competition.drop(columns=["Unnamed 0", "Unnamed 0.1", "Unnamed 0.2", "Unnamed 0.3", "Unnamed 0.4"])
#df_competition.to_csv("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/SPSS/Hypothese Competition stage/dfCompetitionStage.csv")

df_mv = data_prep_teamnumber(pd.read_csv("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/SPSS/Hypothese Market Value/dfMarketValue.csv"))
#df_mv = df_mv.drop(columns=["Unnamed 0", "Unnamed 0.1", "Unnamed 0.2", "Unnamed 0.3", "Unnamed 0.4"])
#df_mv.to_csv("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/SPSS/Hypothese Market Value/dfMarketValue.csv")

df_score= data_prep_teamnumber(pd.read_csv("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/SPSS/Hypothese Score/dfScore.csv"))
#df_score= df_score.drop(columns=["Unnamed 0", "Unnamed 0.1", "Unnamed 0.2", "Unnamed 0.3", "Unnamed 0.4"])
#df_score.to_csv("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/SPSS/Hypothese Score/dfScore.csv")

df_time= data_prep_teamnumber(pd.read_csv("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/SPSS/Hypothese Time/dfTime.csv"))
#df_time = df_time.drop(columns=["Unnamed 0", "Unnamed 0.1", "Unnamed 0.2", "Unnamed 0.3", "Unnamed 0.4"])
#df_time.to_csv("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/SPSS/Hypothese Time/dfTime.csv")




