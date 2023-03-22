import model
from SetUp import CONSTANTS, JSONtoDF

# Set Up


# which attributes should be taken into account?
attributes = CONSTANTS.ATTRIBUTES
#create the model without intercept
log_model_no_interc = CONSTANTS.REGMODELNOINTERC
#with intercept
log_model_interc = CONSTANTS.REGMODELINTERC
#show the summary of the model
model.show_info(log_model_no_interc)
model.show_info(log_model_interc)

# next step is to predict the probability of each shot of the EM2020 and WM2022
# the prediction should be saved to the dataframe and added to the json file


# prediction
# name the model
modelnameInt = CONSTANTS.MODELNAMEINTERCEPT
modelnameNoInt = CONSTANTS.MODELNAMENOINTERCEPT

# EM 2020
dfEM2020 = model.prediction(modelnameInt, log_model_interc, JSONtoDF.createDF(CONSTANTS.JSONEM2020), attributes)
# calculate the accuracy as the difference of statsbomb xg, and my calculation
dfEM2020 = model.calculateAccuracy(modelnameInt, dfEM2020, "EM20")

dfEM2020.to_json(CONSTANTS.JSONEM2020)

dfEM2020 = model.prediction(modelnameNoInt, log_model_no_interc,JSONtoDF.createDF(CONSTANTS.JSONEM2020), attributes)
# calculate the accuracy as the difference of statsbomb xg, and my calculation
dfEM2020 = model.calculateAccuracy(modelnameNoInt, dfEM2020, "EM20")

# WM 2022
dfWM2022 = model.prediction(modelnameInt, log_model_interc, JSONtoDF.createDF(CONSTANTS.JSONWM2022), attributes)
# calculate the accuracy as the difference of statsbomb xg, and my calculation
dfWM2022 = model.calculateAccuracy(modelnameInt, dfWM2022, "WM22")

dfWM2022.to_json(CONSTANTS.JSONWM2022)

dfWM2022 = model.prediction(modelnameNoInt, log_model_no_interc, JSONtoDF.createDF(CONSTANTS.JSONWM2022), attributes)
# calculate the accuracy as the difference of statsbomb xg, and my calculation
dfWM2022 = model.calculateAccuracy(modelnameNoInt, dfWM2022, "WM22")


# save df

# em2020
#dfEM2020.to_json(CONSTANTS.JSONEM2020)

# wm2022
#dfWM2022.to_json(CONSTANTS.JSONWM2022)