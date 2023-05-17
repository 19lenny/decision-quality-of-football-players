import math

import CONSTANTS, JSONtoDF
from Model import create_model, model_info

from SetUp.DecisionEvaluation import evaluate_decision
import numpy as np

def angle(x, y):
    b = ((x - CONSTANTS.X_COORDINATE_POST_L) ** 2 +
             (y - CONSTANTS.Y_COORDINATE_POST_L) ** 2) ** 0.5
    c = ((x - CONSTANTS.X_COORDINATE_POST_R) ** 2 +
             (y - CONSTANTS.Y_COORDINATE_POST_R) ** 2) ** 0.5

    if b == 0 or c == 0:
        return 0, 0, np.log(0.001)
    else:
        test_val = ((b ** 2 + c ** 2 - CONSTANTS.GOAL_LENGTH ** 2)/ (2 * b * c))
        #the arccos for 1 is not defined in python. the result of arccos of 1 should be 0.
        # therefore if the calculation results in 1 (this is a float calculation, therefore we compare it just to 1 on 5 digits after the point)
        # the method returns 0 as degree
        if math.isclose(((b ** 2 + c ** 2 - CONSTANTS.GOAL_LENGTH ** 2)/ (2 * b * c)), 1, abs_tol=1e-5):
            return 0,0,np.log(0.001)
        # the arccos for -1 is not defined in python. the result of arccos of -1 should be 180 degree.
        # therefore if the calculation results in -1 (this is a float calculation, therefore we compare it just to -1 on 5 digits after the point)
        # the method returns 180 as degree
        elif math.isclose(((b ** 2 + c ** 2 - CONSTANTS.GOAL_LENGTH ** 2) / (2 * b * c)), -1, abs_tol=1e-5):
            deg = 180
            rad = np.pi
            ln = np.log(rad)
            return deg, rad, ln
        deg = np.rad2deg(np.arccos((b ** 2 + c ** 2 - CONSTANTS.GOAL_LENGTH ** 2)
                                              / (2 * b * c)))
        rad = np.arccos((b ** 2 + c ** 2 - CONSTANTS.GOAL_LENGTH ** 2)
                                       / (2 * b * c))
        ln = np.log(rad)
        if rad < 0.000001:
            ln = np.log(0.001)

        return deg, rad, ln
ATTRIBUTES = ['distance_to_goal_centre', 'log_angle', 'delta_distance_GK_to_optimal_line']
model = create_model.create_model_glm(JSONtoDF.createDF(CONSTANTS.JSONTRAINSHOTS), ATTRIBUTES)
model_info.show_info(model)

df_return = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
# add xGoal, calculated by me
df_return = model_info.prediction(df_return)
# calculates
# - the xG of the best alternative
# - the x and y coordinate of the best alternative
# - the difference of the shooting players decision and the decision of the best alternative
# - if the shooting player made the best decision
# - the xP of the pass that would be needed to go to the best alternative
df_return = evaluate_decision.decisionEvaluation(df_return, "competition")

# reset the index, so a new index is created
df_return.reset_index(drop=True, inplace=True)
df_return['index'] = df_return.index
df_return.to_json(CONSTANTS.JSONTESTSHOTS)






