from statsbombpy import sb
import pandas as pd
from SetUp import DataManipulation, CONSTANTS, JSONtoDF
from Model import model_info
from SetUp.DecisionEvaluation import evaluate_decision
from SetUp import TM_values

def getDF(competition_id, season_id, competition, save_path):
    df_return = JSONtoDF.createDF(save_path)
    df_return.reset_index(drop=True, inplace=True)


    # before we save the df, we want to add crucial information to the shot,
    # with this information we can later calculate the xG
    # therefore we calculate for every shot, the angle and the distance

    # convert coordinates from list, to x and y entries
    df_return = DataManipulation.coordinates(df_return)
    # add angle
    df_return = DataManipulation.angle(df_return)
    # add angle in rad
    df_return = DataManipulation.angleInRadian(df_return)
    # add the penalty for bad radians
    df_return = DataManipulation.log_angle(df_return)
    # add distance
    df_return = DataManipulation.distancePlayerToGoal(df_return)

    # add xGoal, calculated by me
    df_return = model_info.prediction(df_return)

    # calculates
    # - the xG of the best alternative
    # - the x and y coordinate of the best alternative
    # - the difference of the shooting players decision and the decision of the best alternative
    # - if the shooting player made the best decision
    # - the xP of the pass that would be needed to go to the best alternative
    df_return = evaluate_decision.decisionEvaluation(df_return, competition)

    # reset the index, so a new index is created
    df_return.reset_index(drop=True, inplace=True)

    # convert the df_return to a JSON.
    # this is done for two reasons:
    # 1) security: the provider can change the data all the time, in  downloading to JSON, we work on a hard copy
    # 2) speed: it is way faster to work with data from a JSON file instead of always calling the API
    # Therefore this code only has to be running once, the output is saved in a JSON file
    df_return.to_json(save_path)

    print("i am finished with competition: ", competition)
    return df_return


dfAll = getDF(competition_id=55, season_id=43, competition="all", save_path=CONSTANTS.JSONTESTSHOTS)


