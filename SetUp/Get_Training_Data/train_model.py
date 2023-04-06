from Model import model_info
from SetUp import JSONtoDF
from SetUp import CONSTANTS

# summary of training data
data = JSONtoDF.createDF(CONSTANTS.JSONTRAINSHOTS)
description = data.describe()
print(description)
# create the model
regression = CONSTANTS.REGRESSION_MODEL
# show the info of the model
model_info.show_info(regression=regression)