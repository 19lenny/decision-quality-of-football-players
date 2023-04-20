import numpy as np
import pandas as pd
from Draw import xG_heatmap
from Model import create_model, model_info
from SetUp import JSONtoDF,CONSTANTS, DataManipulation



def angle_to_goal(df):
    angleList = []
    for shot in range(len(df)):
        x_shot = df['x'][shot]
        y_shot = df['y'][shot]
        angle = DataManipulation.angleInRadianFromObjectToPoints(x_object=x_shot, y_object=y_shot,
                                                         x_point1=CONSTANTS.X_COORDINATE_POST1 + 0.0000001,
                                                         x_point2=CONSTANTS.X_COORDINATE_POST2 + 0.0000001,
                                                         y_point1=CONSTANTS.Y_COORDINATE_POST1,
                                                         y_point2=CONSTANTS.Y_COORDINATE_POST2)
        if angle < 0.000001:
            angle = 0.00001
        angleList.append(angle)
    df['angle_to_goal'] = angleList
    return df
def log_penalty(df):
    df = angle_to_goal(df)
    penaltyList = []
    for shot in range(len(df)):
        # if the shot is given between the two posts the penalty should be 0
        if (df['x'][shot] >= 36) and  (df['y'][shot] <= 44):
            #penaltyList.append(0)
            penaltyList.append(-np.log(df['angle_to_goal'][shot]))
        # else a penalty has to be calculated
        else:
            penaltyList.append(-np.log(df['angle_to_goal'][shot]))
    df['log_penalty'] = penaltyList
    return df




def calculate_xG_for_grid(square_meter_size, max_shot_distance, modelname):
    square_meter_size = square_meter_size
    max_shot_distance = max_shot_distance
    # -----------------------------------------------------------------------------------------------------------
    # create a grid which shows for every x and y combination the xGoal according to regression

    x_range_pitch = np.arange(CONSTANTS.X_COORDINATE_GOALCENTRE - max_shot_distance,
                              120.5,
                              square_meter_size)
    # create the y linspace of the pitch, the end value gets +square meter size,
    # such that the endpoint is still in the range
    """
    y_range_pitch = np.arange(CONSTANTS.Y_MIDDLE_LINE1,
                              CONSTANTS.Y_MIDDLE_LINE2 + square_meter_size,
                              square_meter_size)
    """
    y_range_pitch = np.arange(15,
                              65,
                              square_meter_size)

    xGList = []
    xList = []
    yList = []
    angleList = []
    distanceList = []
    for x in x_range_pitch:
        for y in y_range_pitch:
            # if it hit left post go to next iteration
            if (x == 120) & (y == 36):
                xgPrediction = 0
                xList.append(x)
                yList.append(y)
                xGList.append(xgPrediction)
                angle_in_rad = DataManipulation.angleInRadianFromObjectToPoints(x_object=x,
                                                                                y_object=y,
                                                                                x_point1=CONSTANTS.X_COORDINATE_POST1,
                                                                                y_point1=CONSTANTS.Y_COORDINATE_POST1,
                                                                                x_point2=CONSTANTS.X_COORDINATE_POST2,
                                                                                y_point2=CONSTANTS.Y_COORDINATE_POST2)
                distance_in_yards = DataManipulation.distanceObjectToPoint(x_object=x, y_object=y,
                                                                           x_point=CONSTANTS.X_COORDINATE_GOALCENTRE,
                                                                           y_point=CONSTANTS.Y_COORDINATE_GOALCENTRE)
                angleList.append(angle_in_rad)
                distanceList.append(distance_in_yards)
                continue
            # if it hit right post go to next iteration
            elif (x == 120) & (y == 44):
                xgPrediction = 0
                xList.append(x)
                yList.append(y)
                xGList.append(xgPrediction)
                angle_in_rad = DataManipulation.angleInRadianFromObjectToPoints(x_object=x,
                                                                                y_object=y,
                                                                                x_point1=CONSTANTS.X_COORDINATE_POST1,
                                                                                y_point1=CONSTANTS.Y_COORDINATE_POST1,
                                                                                x_point2=CONSTANTS.X_COORDINATE_POST2,
                                                                                y_point2=CONSTANTS.Y_COORDINATE_POST2)
                distance_in_yards = DataManipulation.distanceObjectToPoint(x_object=x, y_object=y,
                                                                           x_point=CONSTANTS.X_COORDINATE_GOALCENTRE,
                                                                           y_point=CONSTANTS.Y_COORDINATE_GOALCENTRE)
                angleList.append(angle_in_rad)
                distanceList.append(distance_in_yards)
                continue
            logmodel = modelname
            x_location = x
            y_location = y

            angle_in_rad = DataManipulation.angleInRadianFromObjectToPoints(x_object=x_location, y_object=y_location,
                                                                            x_point1=CONSTANTS.X_COORDINATE_POST1,
                                                                            y_point1=CONSTANTS.Y_COORDINATE_POST1,
                                                                            x_point2=CONSTANTS.X_COORDINATE_POST2,
                                                                            y_point2=CONSTANTS.Y_COORDINATE_POST2)
            distance_in_yards = DataManipulation.distanceObjectToPoint(x_object=x_location, y_object=y_location,
                                                                       x_point=CONSTANTS.X_COORDINATE_GOALCENTRE,
                                                                       y_point=CONSTANTS.Y_COORDINATE_GOALCENTRE)
            # xG on the current location is the prediction of the expected goal from this location,
            # based on the angle of the location to the goal and the distance of the location to the goal
            # the prediction has to be multiplied with the xPass prediction
            # (the longer the teammate has time, the higher will be xP)
            # therefore max penalty is -5
            if angle_in_rad < 0.000001:
                angle_in_rad = 0.00001
            log_pen = -np.log(angle_in_rad)
            data = [[angle_in_rad, distance_in_yards, log_pen]]
            predictionDf = pd.DataFrame(data, columns=["angleInRadian", "distance_to_goal_centre", "log_penalty"])
            pred = modelname.predict(predictionDf)


            xgPrediction = pred[0]

            xList.append(x)
            yList.append(y)
            xGList.append(xgPrediction)
            angleList.append(angle_in_rad)
            distanceList.append(distance_in_yards)
    data = {'x': xList,
            'y': yList,
            'xGPrediction': xGList,
            'distance': distanceList,
            'angle': angleList
            }
    dfXGGrid = pd.DataFrame(data)
    dfXGGrid = log_penalty(dfXGGrid)
    return dfXGGrid

# shot distance in yards

dfTrain = JSONtoDF.createDF(CONSTANTS.JSONTRAINSHOTS)
dfTrain = dfTrain.rename(columns={"x_coordinate": "x", "y_coordinate": "y"})
dfTrain = log_penalty(dfTrain)
model = create_model.create_model_glm(dfTrain, attributes=['angleInRadian', 'distance_to_goal_centre', 'log_penalty'])
model_info.show_info(model)
xg = calculate_xG_for_grid(square_meter_size=0.5, max_shot_distance=25, modelname=model)
xG_heatmap.draw_xG_model(dfXGGrid=xg, saving_location="C:/Users/lenna/Downloads/model_vis_test.png", title="xGModel_test")

