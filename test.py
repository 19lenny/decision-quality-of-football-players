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
print(len(dfTest['minute']))

dfTest2 = JSONtoDF.createDF("JSON/ShotsEM2020.json")
dfTest2 = dfTest2[(dfTest2['minute'] > 90) & (dfTest2['competition_stage'] == 'Round of 16')]


