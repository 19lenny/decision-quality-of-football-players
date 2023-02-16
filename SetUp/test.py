import pandas as pd
import numpy as np
from statsbombpy import sb

x_ball = 109
y_ball = 40
a_goal_length = 7.32
x_coordinate_post1 = 120
y_coordinate_post1 = 36.34
x_coordinate_post2 = 120
y_coordinate_post2 = 43.66
x_coordinate_goalCentre = 120
y_coordinate_goalCentre = y_coordinate_post1 + a_goal_length / 2

b = ((x_ball - x_coordinate_post1) ** 2 +
     (y_ball - y_coordinate_post1) ** 2) ** 0.5
c= ((x_ball - x_coordinate_post2) ** 2 +
    (y_ball - y_coordinate_post2) ** 2) ** 0.5

testInDegree = np.rad2deg(np.arccos((b ** 2 - c ** 2 - a_goal_length ** 2) / (-2 * c * a_goal_length)))
test2 = np.rad2deg(np.arccos((b**2+c**2-a_goal_length**2)/(2*b*c)))
calcBefore = np.rad2deg(np.arccos((b ** 2 + c ** 2 - a_goal_length ** 2) / (2 * b * c)))

print("debugger")
