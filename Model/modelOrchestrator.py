import model
from SetUp import CONSTANTS

# Set Up

# name the model
modelname = "xGAngleDistance"
# which attributes should be taken into account?
attributes = ['angleInRadian', 'distance_to_goal_centre']
#create the model without intercept
logRegModelLogit = model.create_model_logit(CONSTANTS.JSONMODELALLSHOTS, attributes)
#show the summary of the model
model.show_info(logRegModelLogit)

# next step is to predict the probability of each shot of the EM2020 and WM2022
# the prediction should be saved to the dataframe and added to the json file


# prediction


# EM 2020
dfEM2020 = model.prediction(modelname, logRegModelLogit, CONSTANTS.JSONEM2020, attributes)
# calculate the accuracy as the difference of statsbomb xg, and my calculation
dfEM2020 = model.calculateAccuracy(modelname, dfEM2020)

# WM 2022
dfWM2022 = model.prediction(modelname, logRegModelLogit, CONSTANTS.JSONWM2022, attributes)
# calculate the accuracy as the difference of statsbomb xg, and my calculation
dfWM2022 = model.calculateAccuracy(modelname, dfWM2022)


# save df

# em2020
dfEM2020.to_json(CONSTANTS.JSONEM2020)

# wm2022
dfWM2022.to_json(CONSTANTS.JSONWM2022)
