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
df = JSONtoDF.createDF(CONSTANTS.JSONWM2022)
x = df['x_coordinate'].mean()
y = df['y_coordinate'].mean()
dist = df['distance_to_goal_centre'].mean()


x_location = 114
y_location = 40
logmodel = CONSTANTS.REGMODELINTERC

angle_in_rad = DataManipulation.angleInRadianFromObjectToPoints(x_object=x_location, y_object=y_location,
                                                                x_point1=CONSTANTS.X_COORDINATE_POST1,
                                                                y_point1=CONSTANTS.Y_COORDINATE_POST1,
                                                                x_point2=CONSTANTS.X_COORDINATE_POST2,
                                                                y_point2=CONSTANTS.Y_COORDINATE_POST2)
distance_in_yards = DataManipulation.distanceObjectToPoint(x_object=x_location, y_object=y_location,
                                                           x_point=CONSTANTS.X_COORDINATE_GOALCENTRE,
                                                           y_point=CONSTANTS.Y_COORDINATE_GOALCENTRE)
prediction = model.predictionOfSingleValues([angle_in_rad, distance_in_yards], CONSTANTS.ATTRIBUTES, logmodel)
predictionNOIntercept = model.predictionOfSingleValues([angle_in_rad, distance_in_yards], CONSTANTS.ATTRIBUTES, CONSTANTS.REGMODELNOINTERC)


model.show_info(CONSTANTS.REGMODELINTERC)
model.show_info(CONSTANTS.REGMODELNOINTERC)




