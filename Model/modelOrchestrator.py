import model

# first we have to create a model on all Shot Data (except the one we are evaluating)
logRegModel = model.create_model(
    "G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/JSON/allModelData.json")

# next step is to show the info of the model
model.show_info(logRegModel)

# next step is to predict the probability of each shot of the EM2020 and WM2022
# the prediction should be saved to the dataframe and added to the json file

# test of Angle and Distance
modelname = "xGAngleDistance"
attributes = ['angle', 'distance_to_goal_centre']

# EM 2020
dfEM2020 = model.prediction(modelname, logRegModel,
                            'G:/Meine Ablage/a_uni 10. Semester - '
                            'Masterarbeit/Masterarbeit/Thesis/thesis/JSON/ShotsEM2020.json', attributes)
dfEM2020 = model.calculateAccuracy(modelname, dfEM2020)
# savedf
dfEM2020.reset_index(inplace=True)
dfEM2020.to_json(
    'G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/JSON/ShotsEM2020.json')

# WM 2022
dfWM2022 = model.prediction(modelname, logRegModel,
                            'G:/Meine Ablage/a_uni 10. Semester - '
                            'Masterarbeit/Masterarbeit/Thesis/thesis/JSON/ShotsWM2022.json', attributes)
dfWM2022 = model.calculateAccuracy(modelname, dfWM2022)
# savedf
dfWM2022.reset_index(inplace=True)
dfWM2022.to_json(
    'G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/JSON/ShotsWM2022.json')
