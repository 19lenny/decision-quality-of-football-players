from SetUp import CONSTANTS, JSONtoDF
from Model import create_model, model_info
from SetUp.DecisionEvaluation import evaluate_decision

# this file calculates the model and applies it to the test set
# the data was downloaded before that and is saved in a json format


# the model needs now to be applied to every square yard for every shot
# for this the xP model was slightly changed
dfTest_ball_speed_40 = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
dfTest_ball_speed_40.reset_index(drop=True, inplace=True)
dfTest_ball_speed_40 = evaluate_decision.decisionEvaluation(dfSeason=dfTest_ball_speed_40, eventname="decisionAlternatives")
# reset the index, so a new index is created
dfTest_ball_speed_40.reset_index(drop=True, inplace=True)

# convert the df Test with all new calculations to a JSON.

dfTest_ball_speed_40.to_json("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/SPSS/Robustness Check/ball speed 40.5/dfTest_ballspeed_40.json")


print("i am finished with ball speed , change ball speed again to 38.52")
