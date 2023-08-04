from SetUp import CONSTANTS,JSONtoDF
from SetUp.DecisionEvaluation import evaluationHelper

dfTrain = JSONtoDF.createDF(CONSTANTS.JSONTRAINSHOTS)
dfTest = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
train_descr = dfTrain.describe()
test_descr = dfTest.describe()
