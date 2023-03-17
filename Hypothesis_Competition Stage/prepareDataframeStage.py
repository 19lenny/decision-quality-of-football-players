from typing import List
from scipy.stats import ttest_ind
import pandas as pd
from SetUp import JSONtoDF, CONSTANTS
from statistics import mean


# the goal is only to evaluate teams that were represented in the group stage and in the knockout phase
# for this we have to manipulate the data a bit
def KOvsGroupStage(df, name_KO_stage):

    # create a dataframe with all teams that achieved the round of 16
    # this searches for the teams and drops all duplicates, since a team cannot achieve multiple time
    KO_stage = df[["home_team", "away_team"]][df['competition_stage'] == name_KO_stage].drop_duplicates()
    KO_stage = pd.concat([KO_stage['home_team'], KO_stage['away_team'].rename({'away_team': 'home_team'})])
    KO_stage = KO_stage.values.tolist()

    # keep only shots of teams that are in list of the round of 16
    dfManipulated = df[df['team'].isin(KO_stage)]
    dfManipulated.reset_index(inplace=True)
    dfManipulated.drop(["level_0", "index"], axis=1)
    return dfManipulated

def TeamsInStage(df, name_KO_stage):

    # create a dataframe with all teams that achieved the round of 16
    # this searches for the teams and drops all duplicates, since a team cannot achieve multiple time
    KO_stage = df[["home_team", "away_team"]][df['competition_stage'] == name_KO_stage].drop_duplicates()
    KO_stage = pd.concat([KO_stage['home_team'], KO_stage['away_team'].rename({'away_team': 'home_team'})])
    KO_stage = KO_stage.values.tolist()

    return KO_stage

def tTestResults(df):
    ko_stages = ["Round of 16", "Quarter-finals", "Semi-finals", "Final"]

    # create empty lists, that can be filled later
    t_stat: List[float] = [0.0] * len(ko_stages)
    p_values: List[float] = [0.0] * len(ko_stages)
    current_highest_stage: List[str] = [''] * len(ko_stages)
    meanOne: List[float] = [0.0] * len(ko_stages)
    meanTwo: List[float] = [0.0] * len(ko_stages)
    # H0: the competitors of the current highest competition stage
    # have done the same decision in the upcoming competition stages compared to the played ones before
    for index in range(len(ko_stages)):

        # we manipulate the dataframes in a way that only the shots of the teams count,
        # that achieved the current highest competition round
        dfShotEval = KOvsGroupStage(df, ko_stages[index])


        # create group stage df and transform it to a list
        # when the list is empty then we are in the group stage, if the list is starting, we compare
        # [:index] everything until but excluding the index number
        # therefore if index is 0, then the list is empty and we know that we are in the group stage
        # first iteration: group stage vs KO stage
        # second iteration: group stage + Round of 16  vs. "Quarter-finals", "Semi-finals", "Final"
        # third iteration: group stage + Ro16 + QF vs. Semi-Finals + Final
        # fourth iteration: GS + Ro16 + QF + SF vs. Final
        # in dfShotEval it is ensured that only the shots are taken into account,
        # that are coming from teams, that achieved the current highest competition stage
        isGroupStage = not bool(ko_stages[:index])
        if isGroupStage:
            current_stages_df = dfShotEval.loc[dfShotEval['competition_stage'] == "Group Stage"]
        else:
            # competition stage is either group stage or one of the other ko stages
            current_stages_df = dfShotEval.loc[
                dfShotEval['competition_stage'].isin(["Group Stage"] + ko_stages[:index])]
        shotValuesCurrentStages = current_stages_df['xG_Delta_decision_alternative'].values.tolist()

        meanOne[index] = mean(shotValuesCurrentStages)

        # create df for all remaining knock out stages and create a list from it
        # [index:] including the index until the end
        ko_stage_df = dfShotEval.loc[dfShotEval['competition_stage'].isin(ko_stages[index:])]
        shotValuesRemainingStages = ko_stage_df['xG_Delta_decision_alternative'].values.tolist()

        meanTwo[index] = mean(shotValuesRemainingStages)

        t_stat[index], p_values[index] = ttest_ind(shotValuesCurrentStages, shotValuesRemainingStages)
        current_highest_stage[index] = "Group Phase, " + str(', '.join(ko_stages[:index])) +" vs. "+ str(', '.join(ko_stages[index:]))

    # save the created lists to a dataframe
    dataCompetitionStage = {'competition_separator': current_highest_stage,
                            'T-stat': t_stat,
                            'P-Val': p_values,
                            'mean_xG_Delta_low_competition': meanOne,
                            'mean_xG_Delta_high_competition': meanTwo}
    dfCompStage = pd.DataFrame(dataCompetitionStage)
    return dfCompStage