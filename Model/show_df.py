from SetUp import CONSTANTS,JSONtoDF
from SetUp.DecisionEvaluation import evaluationHelper

dfTrain = JSONtoDF.createDF(CONSTANTS.JSONTRAINSHOTS)
dfTest = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)

#test