from Model import create_model
from SetUp import JSONtoDF

# File paths

#Where the JSON are stored
#only file name has to be added
JSONFILEPATH = "G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/JSON/"
JSONBACKUPFOLDER = "G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/JSON/BackUp/"
JSONDECEVA= "G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/DecisionEvaluation/"
JSONEM2020 = "G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/JSON/ShotsEM2020.json"
JSONWM2018 = "G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/JSON/ShotsWM2018.json"
JSONWM2022 = "G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/JSON/ShotsWM2022.json"
JSONTRAINSHOTS = "G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/" \
                    "Masterarbeit/Thesis/thesis/JSON/Train_Set_Shots.json"
JSONTESTSHOTS = "G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/" \
                    "Masterarbeit/Thesis/thesis/JSON/Test_Set_Shots.json"
JSONSHOTEVALUATIONEM2020 =\
    "G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/" \
    "JSON/Evaluation/ShotEvaluationEM20INT.json"
JSONSHOTEVALUATIONWM2022 =\
    "G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/" \
    "JSON/Evaluation/ShotEvaluationWM22INT.json"


# locations

# x and y coordinates do not have to be transformed:
# https://www.bundesliga.com/en/faq/all-you-need-to-know-about-soccer/all-you-need-to-know-about-a-soccer-field-10572
# these are the official coordinates of statsbomb.
# they official disclosures can be found in statsbomb Open Data specification v1.pdf
# https://github.com/statsbomb/statsbombpy/blob/master/doc/StatsBomb%20Open%20Data%20Specification%20v1.1.pdf
# all values in yards
GOAL_LENGTH = 8
X_COORDINATE_POST1 = 120
Y_COORDINATE_POST1 = 36
X_COORDINATE_POST2 = 120
Y_COORDINATE_POST2 = 44
X_COORDINATE_GOALCENTRE = 120
Y_COORDINATE_GOALCENTRE = 40
X_MIDDLE_LINE = 60
Y_MIDDLE_LINE1 = 0
Y_MIDDLE_LINE2 = 80


# speed (in yards / second)
# 38.52 km/h
# from km/h to yards/second
FROMKMHTOYPS = 0.30378147176
BALL_SPEED = 38.52 * FROMKMHTOYPS
# 19.8 km/h
PLAYER_SPEED = 19.8 * FROMKMHTOYPS


# logistic model

#logmodel should also not change after it is calculated once
# which attributes should be taken into account?
ATTRIBUTES = ['angleInRadian', 'distance_to_goal_centre']

# model with intercept
MODELNAMEINTERCEPT = "xG"

df = JSONtoDF.createDF(JSONTRAINSHOTS)
REGMODELINTERC = create_model.create_model_glm(JSONtoDF.createDF(JSONTRAINSHOTS), ATTRIBUTES)

#this is the current Model
MODELNAME = MODELNAMEINTERCEPT
REGRESSION_MODEL = REGMODELINTERC

#normal distribution
EVALUATION_VARIABLE = "xG_Delta_decision_alternative"

