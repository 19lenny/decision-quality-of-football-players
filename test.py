from SetUp import JSONtoDF, DataManipulation, CONSTANTS
import pandas as pd
import json
import os
import numpy as np
from DecisionEvaluation import evaluationHelper
from SetUp import CONSTANTS, JSONtoDF
import pandas as pd
from Model import  model


# todo: it has to be checked why distance is farther away as it should be
df = JSONtoDF.createDF(CONSTANTS.JSONEM2020)
x = df['x_coordinate'].mean()
y = df['y_coordinate'].mean()
dist = df['distance_to_goal_centre'].mean()

dfINT = JSONtoDF.createDF((CONSTANTS.JSONFILEPATH+"ShotEvaluationWM22ReadableINT.json"))
dfNoInt = JSONtoDF.createDF((CONSTANTS.JSONFILEPATH+"ShotEvaluationEM2020ReadableNOINT.json"))

print("number of x_coordinate == 120: ", len(dfINT[dfINT['x_best_alt'] == 120]))
print("number of x_coordinate == 0: ", len(dfINT[dfINT['x_best_alt'] == 0]))
print("number of all shots at EM2020: ", len(dfINT['minute']))
print("number of right decision: ", len(dfINT[dfINT['shot_decision_correct'] == True]))
print("number of wrong decision: ", len(dfINT[dfINT['shot_decision_correct'] == False]))

print("-------------------------------------------------------------------------")
print("number of x_coordinate == 120: ", len(dfNoInt[dfNoInt['x_best_alt'] == 120]))
print("number of x_coordinate == 0: ", len(dfNoInt[dfNoInt['x_best_alt'] == 0]))
print("number of all shots at EM2020: ", len(dfNoInt['minute']))
print("number of right decision: ", len(dfNoInt[dfNoInt['shot_decision_correct'] == True]))
print("number of wrong decision: ", len(dfNoInt[dfNoInt['shot_decision_correct'] == False]))


