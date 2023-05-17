from statsbombpy import sb
import pandas as pd
from SetUp import DataManipulation, CONSTANTS, joinDF
from Model import model_info
from SetUp.DecisionEvaluation import evaluate_decision
from SetUp import TM_values

def getDF(competition_id, season_id, competition):
    df_matches = pd.DataFrame(sb.matches(competition_id, season_id))
    df_matches = df_matches.sort_values(by=['match_id'])
    df_matches.reset_index(drop=True, inplace=True)
    # all matchID's of the current competition
    match_ids = df_matches.match_id.values.tolist()

    # initialize df
    dfEvents = pd.DataFrame()
    # this must be done for every event in every game,
    # then we have a dataframe with all shots from every game from the current competition
    counter = 0
    for event in match_ids:
        get_all_events_of_this_match = sb.events(event)
        dfEvents = pd.concat([dfEvents, get_all_events_of_this_match])
        counter += 1
        print("nothing to worry - still working")
        print("progress bar to get all events at ", competition, ": ", counter, " / ", len(match_ids))

    # set the key index for the join later
    df_matches.set_index("match_id")

    # join Shots and Matches, therefore we know from every score the competition stage,
    # the competition and additional information
    df_return = dfEvents.join(df_matches.set_index('match_id'), on='match_id')
    df_return.reset_index(drop=True, inplace=True)

    # add the score, this has to be done here, because there is the possibility of own goals
    df_return = DataManipulation.addGoalBinary(df_return)
    # add the current score of this competition
    df_return = DataManipulation.score(df_return)
    df_return = df_return.query("type == 'Shot'")
    df_return.reset_index(drop=True, inplace=True)
    print("score is done")

    # before we save the df, we want to add crucial information to the shot,
    # with this information we can later calculate the xG
    # therefore we calculate for every shot, the angle and the distance

    # convert coordinates from list, to x and y entries
    df_return = DataManipulation.coordinates(df_return)
    # add angle
    df_return = DataManipulation.angleDeg(df_return)
    # add angle in rad
    df_return = DataManipulation.angleInRadian(df_return)
    # add the penalty for bad radians
    df_return = DataManipulation.log_angle(df_return)
    # add distance
    df_return = DataManipulation.distancePlayerToGoal(df_return)

    # add xGoal, calculated by me
    #df_return = model_info.prediction(df_return)

    # only keep the necessery rows, which have something to do with shots and are not from penalties or freekicks
    # this way some time is saved in the next call
    df_return = df_return.query(
        "type == 'Shot' & shot_body_part != 'Head' & shot_type == 'Open Play'")
    df_return.reset_index(drop=True, inplace=True)

    # add the transfer value of every shooting player
    df_return = TM_values.transfermarketValue(dfCompetition=df_return, competition=competition)
    print("TM Value is added")

    # calculates
    # - the xG of the best alternative
    # - the x and y coordinate of the best alternative
    # - the difference of the shooting players decision and the decision of the best alternative
    # - if the shooting player made the best decision
    # - the xP of the pass that would be needed to go to the best alternative
    #df_return = evaluate_decision.decisionEvaluation(df_return, competition)

    # reset the index, so a new index is created
    df_return.reset_index(drop=True, inplace=True)



    print("i am finished with competition: ", competition)
    return df_return

#get EM20
dfEM = getDF(competition_id=55, season_id=43, competition="EM20")

#get WM18
dfWM18 = getDF(competition_id=43, season_id=3, competition="WM18")

#getWM22
dfWM22 = getDF(competition_id=43, season_id=106, competition="WM22")
# concat the testing data
dfAll = joinDF.concat([dfEM, dfWM18, dfWM22])
dfAll.reset_index(drop=True, inplace=True)

# save it
dfAll.to_json("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/BackUp/TestData/dfTest_backup.json")
