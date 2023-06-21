from SetUp import CONSTANTS, JSONtoDF
from Model import create_model, model_info
from SetUp.DecisionEvaluation import evaluate_decision

# this file calculates the model and applies it to the test set
# the data was downloaded before that and is saved in a json format

#read the shots that are used to train the model
dfTrain = JSONtoDF.createDF(CONSTANTS.JSONTRAINSHOTS)
#train the model, the model includes the intercept
reg_model = create_model.create_model_glm(df=dfTrain, attributes=CONSTANTS.ATTRIBUTES)
#show the infor of the model
model_info.show_info(regression=reg_model)

# the model was saved to a global variable, therefore it is not needed to hand it to the train dataframe.
# the model needs now to be applied to every square yard for every shot
dfTest = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
dfTest.reset_index(drop=True, inplace=True)
dfTest = evaluate_decision.decisionEvaluation(dfSeason=dfTest, eventname="decisionAlternatives")
# reset the index, so a new index is created
dfTest.reset_index(drop=True, inplace=True)

# convert the df Test with all new calculations to a JSON.

dfTest.to_json(CONSTANTS.JSONTESTSHOTS)

print("i am finished with MAIN")

