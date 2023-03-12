import pandas as pd
import prepareDataframeScore
from SetUp import JSONtoDF, CONSTANTS, DataManipulation
from DecisionEvaluation import evalDecInterc_XG_delta
from Model import model
from SetUp import CONSTANTS

# add xG to all shots of EM2020
# which attributes should be taken into account?
attributes = CONSTANTS.ATTRIBUTES
#with intercept
log_model_interc = CONSTANTS.REGMODELINTERC
# next step is to predict the probability of each shot of the EM2020 and WM2022
# the prediction should be saved to the dataframe and added to the json file
# prediction
# name the model
modelnameInt = CONSTANTS.MODELNAMEINTERCEPT

# calculate the scores
dfEMScore = JSONtoDF.createDF("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/"
                              "Thesis/thesis/Hypothesis_Score/ShotsEM2020.json")
dfEMScore = DataManipulation.score(dfEMScore)
dfEMScore = dfEMScore.query("shot_body_part != 'Head' & play_pattern != 'From Free Kick' & shot_type != 'Penalty'")
dfEMScore.reset_index(drop=True, inplace=True)
# EM 2020, add the expected goals for every shot
dfEMScore = model.prediction(modelnameInt, log_model_interc, dfEMScore, attributes)
# calculate the accuracy as the difference of statsbomb xg, and my calculation
dfEMScore = model.calculateAccuracy(modelnameInt, dfEMScore)

print(len(dfEMScore['minute']))
# check for every shot if the shooter made the right decision
dfEMScore = evalDecInterc_XG_delta.XGdifference(dfEMScore, "G:/Meine Ablage/"
                                                           "a_uni 10. Semester - Masterarbeit/"
                                                           "Masterarbeit/Thesis/thesis/Hypothesis_Score/EM20")

#save the results
dfEMScore.to_json("ScoreEM2020.json")


# calculate the scores
dfWMScore = JSONtoDF.createDF("G:/Meine Ablage/"
                              "a_uni 10. Semester - Masterarbeit/Masterarbeit"
                              "/Thesis/thesis/Hypothesis_Score/ShotsWM2022.json")
dfWMScore = DataManipulation.score(dfWMScore)
dfWMScore = dfWMScore.query("shot_body_part != 'Head' & play_pattern != 'From Free Kick' & shot_type != 'Penalty'")
dfWMScore.reset_index(drop=True, inplace=True)
# WM 2022, add the expected goals for every shot
dfWMScore = model.prediction(modelnameInt, log_model_interc, dfWMScore, attributes)
# calculate the accuracy as the difference of statsbomb xg, and my calculation
dfWMScore = model.calculateAccuracy(modelnameInt, dfWMScore)

print(len(dfWMScore['minute']))
# check for every shot if the shooter made the right decision
dfWMScore = evalDecInterc_XG_delta.XGdifference(dfWMScore, "G:/Meine Ablage/"
                                                           "a_uni 10. Semester - Masterarbeit/"
                                                           "Masterarbeit/Thesis/thesis/Hypothesis_Score/WM22")

#save the results
dfWMScore.to_json("ScoreWM2022.json")


