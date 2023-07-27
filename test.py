from SetUp import CONSTANTS, JSONtoDF
from Model import create_model, model_info
from SetUp.DecisionEvaluation import evaluate_decision




# the model was saved to a global variable, therefore it is not needed to hand it to the train dataframe.
# the model needs now to be applied to every square yard for every shot
dfTest = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
dfTest.reset_index(drop=True, inplace=True)

#dfTest.to_json(CONSTANTS.JSONTESTSHOTS)

print("i am finished with MAIN")

