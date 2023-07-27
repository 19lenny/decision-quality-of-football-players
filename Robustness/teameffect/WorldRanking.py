from typing import List

import pandas as pd
from SetUp import CONSTANTS, JSONtoDF
#import all fifa men ranking tables since 1992
menRanking = pd.read_csv('G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Robustness/teameffect/Fifa Men Ranking.csv')
menRanking["country"] = menRanking["country"].replace("Korea Republic", "South Korea")
menRanking["country"] = menRanking["country"].replace("IR Iran", "Iran")
menRanking["country"] = menRanking["country"].replace("USA", "United States")

#only keep three of these tables, store it in df
#always take the ranking table that is the closest

men_ranking_wc2022 = menRanking.loc[(menRanking['date'] == '2022-10-06')]
men_ranking_wc2022.reset_index(drop=True, inplace=True)

men_ranking_euros2020 = menRanking.loc[(menRanking['date'] == '2021-05-27')]
men_ranking_euros2020.reset_index(drop=True, inplace=True)

men_ranking_wc2018 = menRanking.loc[(menRanking['date'] == '2018-06-07')]
men_ranking_wc2018.reset_index(drop=True, inplace=True)

#read the dataframe with every shot (in the first and second half)
df_shots = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
df_shots.reset_index(drop=True, inplace=True)

points: List[int] = [0] * len(df_shots)
own_scoring_difference: List[int] = [0] * len(df_shots)
#add the points of every team to the dataframe. the points come from the mens ranking with respect to the date
for shot in range(len(df_shots)):
    competition = df_shots['season'][shot]
    team = df_shots['team'][shot]
    print(shot)
    if competition == 2018:
        row = men_ranking_wc2018.loc[(men_ranking_wc2018['country']) == team]
        row.reset_index(drop=True, inplace=True)
        points[shot] = row['totalPoints'][0]
    elif competition == 2020:
        row = men_ranking_euros2020.loc[(men_ranking_euros2020['country']) == team]
        row.reset_index(drop=True, inplace=True)
        points[shot] = row['totalPoints'][0]
    elif competition == 2022:
        row = men_ranking_wc2022.loc[(men_ranking_wc2022['country']) == team]
        row.reset_index(drop=True, inplace=True)
        points[shot] = row['totalPoints'][0]

    #we need one additional point. for the score it is only saved if a team is winning, loosing or drawing and
    # by how many goals the home team is winning or loosing
    #but for this regression we need additionally the own scoring difference, therefore how many points are one in the lead

    # if our team is currently winning, than also the scoring difference has to be positive
    score = df_shots['score'][shot]
    scoring_difference_between_home_away = df_shots['scoring_difference'][shot]
    if score > 0:
        # now check if the scoring difference is positive, if so, write the positive score to the list
        # if not it means that the winning team is the away team, the minus sign of the scoring difference has to be flipped and added to the list
        own_scoring_difference[shot] = abs(scoring_difference_between_home_away)
    elif score < 0:
        # now we are loosing, therefore the scoring difference has to be negative
        if scoring_difference_between_home_away < 0:
            own_scoring_difference[shot] = scoring_difference_between_home_away
        # if this is not the case it needs to be done negative
        else: own_scoring_difference[shot] = scoring_difference_between_home_away*-1

df_shots['team_strength'] = points
df_shots['scoring_difference_shooting_team'] = own_scoring_difference
df_shots.to_csv('G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/SPSS/Robustness Check/teameffect/df_including_teameffect.csv')