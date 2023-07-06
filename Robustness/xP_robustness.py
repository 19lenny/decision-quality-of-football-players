from SetUp import CONSTANTS, JSONtoDF
from Model import create_model, model_info
from SetUp.DecisionEvaluation import evaluate_decision

# this file calculates the model and applies it to the test set
# the data was downloaded before that and is saved in a json format


# the model needs now to be applied to every square yard for every shot
# for this the xP model was slightly changed
dfTest_lamda_three_three = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
dfTest_lamda_three_three.reset_index(drop=True, inplace=True)
dfTest_lamda_three_three = evaluate_decision.decisionEvaluation(dfSeason=dfTest_lamda_three_three, eventname="decisionAlternatives")
# reset the index, so a new index is created
dfTest_lamda_three_three.reset_index(drop=True, inplace=True)

# convert the df Test with all new calculations to a JSON.

dfTest_lamda_three_three.to_json("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/SPSS/Robustness Check/xP lambda 3.3/dfTest_lambda3.json")



