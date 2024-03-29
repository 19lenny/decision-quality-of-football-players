

import pandas as pd
from Model import model_info
from SetUp import JSONtoDF, DataManipulation, CONSTANTS
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import rcParams


def calculate_xG_for_grid(square_meter_size, max_shot_distance, modelname):
    square_meter_size = square_meter_size
    max_shot_distance = max_shot_distance
    # -----------------------------------------------------------------------------------------------------------
    # create a grid which shows for every x and y combination the xGoal according to regression

    x_range_pitch = np.arange(95,
                              120.5,
                              square_meter_size)
    # create the y linspace of the pitch, the end value gets +square meter size,
    # such that the endpoint is still in the range
    """
    y_range_pitch = np.arange(CONSTANTS.Y_MIDDLE_LINE1,
                              CONSTANTS.Y_MIDDLE_LINE2 + square_meter_size,
                              square_meter_size)
    """
    y_range_pitch = np.arange(9,
                              71+square_meter_size,
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
                                                                                x_point1=CONSTANTS.X_COORDINATE_POST_L,
                                                                                y_point1=CONSTANTS.Y_COORDINATE_POST_L,
                                                                                x_point2=CONSTANTS.X_COORDINATE_POST_R,
                                                                                y_point2=CONSTANTS.Y_COORDINATE_POST_R)
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
                                                                                x_point1=CONSTANTS.X_COORDINATE_POST_L,
                                                                                y_point1=CONSTANTS.Y_COORDINATE_POST_L,
                                                                                x_point2=CONSTANTS.X_COORDINATE_POST_R,
                                                                                y_point2=CONSTANTS.Y_COORDINATE_POST_R)
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
                                                                            x_point1=CONSTANTS.X_COORDINATE_POST_L,
                                                                            y_point1=CONSTANTS.Y_COORDINATE_POST_L,
                                                                            x_point2=CONSTANTS.X_COORDINATE_POST_R,
                                                                            y_point2=CONSTANTS.Y_COORDINATE_POST_R)
            distance_in_yards = DataManipulation.distanceObjectToPoint(x_object=x_location, y_object=y_location,
                                                                       x_point=CONSTANTS.X_COORDINATE_GOALCENTRE,
                                                                       y_point=CONSTANTS.Y_COORDINATE_GOALCENTRE)
            log_angle = DataManipulation.log_angle_single_values(angle=angle_in_rad)
            #GK distance = 0 because it is irreleveant for the gK where he is standing for this plot
            GK_delta = 0
            # xG on the current location is the prediction of the expected goal from this location,
            # based on the angle of the location to the goal and the distance of the location to the goal
            # the prediction has to be multiplied with the xPass prediction
            # (the longer the teammate has time, the higher will be xP)
            xgPrediction = model_info.predictionOfSingleValues([distance_in_yards, log_angle, GK_delta], attributes=CONSTANTS.ATTRIBUTES)

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
    return dfXGGrid
"""
What’s going on here? Looking at the Z data first, I’ve merely used the pivot_table method from pandas to cast my data 
into a matrix format, where the columns/rows correspond to the values of Z for each of the points in the range of the 
x-y-axes.
"""
def draw_xG_model(dfXGGrid, saving_location, title):
    dfXGGrid = dfXGGrid[['x', 'y', 'xGPrediction']]
    Z = dfXGGrid.pivot_table(index='x', columns='y', values='xGPrediction').T.values

    X_unique = np.sort(dfXGGrid.x.unique())
    Y_unique = np.sort(dfXGGrid.y.unique())
    X, Y = np.meshgrid(X_unique, Y_unique)
    # Initialize plot objects
    rcParams['figure.figsize'] = 6, 10  # sets plot size
    plt.rcParams["figure.autolayout"] = True

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    img = plt.imread("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Draw/background_pitch/95_120_09_71_bigpenalty.png")
    ax.imshow(img, interpolation='nearest', alpha=1,extent=[95, 120, 9, 71])
    #levels = np.linspace(Z.min(), Z.max(), 14)


    # Generate a color mapping of the levels we've specified

    cpf = ax.contourf(X, Y, Z, levels= [0,0.07, 0.15, 0.3, 1],
                      colors=['#7FD166','#F6EE00', '#FD8300','#D91000'], alpha=0.85, antialiased = True)

    # Set all level lines to black
    line_colors = ['white' for l in cpf.levels]

    # Make plot and customize axes
    #cp = ax.contour(X, Y, Z, levels= [0.07, 0.15, 0.30,], colors= line_colors)
    #ax.clabel(cp, fontsize=12)
    ax.invert_yaxis()
    ax.set_xlabel('x coordinate')
    _ = ax.set_ylabel('y coordinate')
    plt.title(title, fontdict={'fontsize': 20})
    plt.colorbar(cpf, aspect=50)
    fig.tight_layout()
    plt.savefig(saving_location)
    plt.show()

def df_goals_divided_by_shots():
    shots_model = JSONtoDF.createDF(CONSTANTS.JSONTRAINSHOTS)

    shots_model.reset_index(drop=True, inplace=True)

    # dataframe where all the shots happened
    shots_model = shots_model[['goal', 'x_coordinate', 'y_coordinate', 'angleDeg',
                               'angleInRadian', 'distance_to_goal_centre', 'shot_statsbomb_xg']]

    square_meter_size = 1
    max_shot_distance = 25
    # -----------------------------------------------------------------------------------------------------------
    # create a grid which shows for every x and y combination the xGoal according to regression

    # create a grid with a certain amount of bins
    x_range_pitch = np.arange(CONSTANTS.X_COORDINATE_GOALCENTRE - max_shot_distance,
                              CONSTANTS.X_COORDINATE_GOALCENTRE+2*square_meter_size,
                              square_meter_size)
    # create the y linspace of the pitch, the end value gets +square meter size,
    # such that the endpoint is still in the range
    """
    y_range_pitch = np.arange(CONSTANTS.Y_MIDDLE_LINE1,
                              CONSTANTS.Y_MIDDLE_LINE2 + square_meter_size,
                              square_meter_size)
    """
    # this means shots made from the corner flag are not included in the visualization
    y_range_pitch = np.arange(9,
                              71,
                              square_meter_size)

    xGList = []
    xList = []
    yList = []

    for x in range(len(x_range_pitch) - 1):
        for y in range(len(y_range_pitch) - 1):
            number_of_shots_current_location = 0
            number_of_goals_current_location = 0
            xList_current = []
            yList_current = []
            xGList_current = []

            for shot in range(len(shots_model)):
                a = shots_model['x_coordinate'][shot]
                b = x_range_pitch[x]
                c = x_range_pitch[x+1]
                if b == 119:
                     print("deb")
                if (shots_model['x_coordinate'][shot] >= x_range_pitch[x]) and (shots_model['x_coordinate'][shot] < x_range_pitch[x + 1]):
                    if (shots_model['y_coordinate'][shot] >= y_range_pitch[y]) and (
                            shots_model['y_coordinate'][shot] < y_range_pitch[y + 1]):
                        #print("now the shot is good")
                        number_of_shots_current_location += 1
                        if shots_model['goal'][shot] == 1:
                            print("golazooo")
                            number_of_goals_current_location += 1
                        xList_current.append(int(shots_model['x_coordinate'][shot]))
                        yList_current.append(int(shots_model['y_coordinate'][shot]))
            for prob in range(len(xList_current)):
                xGList_current.append(number_of_goals_current_location / number_of_shots_current_location)

            xList = xList + xList_current
            yList = yList + yList_current
            xGList = xGList + xGList_current

    data = {'x': xList,
            'y': yList,
            'xGPrediction': xGList,
            }
    dfXGGrid = pd.DataFrame(data)
    return dfXGGrid

# calculate for every x and y coordinate the xGoal
# shot distance in yards
#xG_grid = calculate_xG_for_grid(square_meter_size=0.5, max_shot_distance=25, modelname=CONSTANTS.REGRESSION_MODEL)
#draw the xG histogram
#draw_xG_model(dfXGGrid=xG_grid, saving_location="C:/Users/lenna/Downloads/model_vis.png", title="xGModel")
print("i printed the xG model map")
dfDivisioned = df_goals_divided_by_shots()
draw_xG_model(dfXGGrid=dfDivisioned, saving_location="C:/Users/lenna/Downloads/goals_divided_by_shots.png", title="goals per shots per location")
