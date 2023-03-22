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

dfEM20 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONEM2020)
dfWM22 = JSONtoDF.createDF(CONSTANTS.JSONSHOTEVALUATIONWM2022)
dfTest = dfWM22[(dfWM22['minute'] == 45) & (dfWM22['competition_stage'] == 'Group Stage')]


dfTest2 = JSONtoDF.createDF("JSON/ShotsEM2020.json")
dfTest2 = dfTest2[(dfTest2['minute'] > 90) & (dfTest2['competition_stage'] == 'Round of 16')]

dfEM20 = DataManipulation.score(dfEM20)


square_meter_size = 1
max_shot_distance = 40
bin_size = 20
print((CONSTANTS.X_COORDINATE_GOALCENTRE + square_meter_size))
print(CONSTANTS.X_COORDINATE_GOALCENTRE - max_shot_distance)

# -----------------------------------------------------------------------------------------------------------
# create a grid with a certain amount of bins
x_range_pitch = np.arange(CONSTANTS.X_COORDINATE_GOALCENTRE - max_shot_distance,
                          CONSTANTS.X_COORDINATE_GOALCENTRE + square_meter_size,
                            square_meter_size)