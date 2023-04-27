import math
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import norm
import DataManipulation, CONSTANTS, JSONtoDF
from SetUp.DecisionEvaluation import evaluationHelper
"""
dfTraining = JSONtoDF.createDF(CONSTANTS.JSONTRAINSHOTS).head(2)
distance_from_line = []
for shot in range(len(dfTraining)):
    #check if dfTraining every shot has a freeze frame, if not it can be forgotten to take players movement in to account
    # kann in backup datei nachgeschaut werden
    #other possbility would be to throw out the shots that have no freeze frame
    #dfOtherPlayers = evaluationHelper.getPlayersOfEvent(dfTraining['shot_freeze_frame'][shot], "Train")
    #find GK of current shot
    for player in range(len(dfOtherPlayers)):
        x = player


#intersection = DataManipulation.intersection_point_GK_Shot(GK, S)
#distance = DataManipulation.distanceObjectToPoint(x_object=GK[0], y_object=GK[1], x_point=intersection[0], y_point=intersection[1])

"""

