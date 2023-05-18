import pandas as pd
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