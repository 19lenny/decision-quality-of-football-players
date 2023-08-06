import math

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Arc
import numpy as np
from SetUp import CONSTANTS, JSONtoDF, DataManipulation

df_test = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
#wm 22 switzerland vs brazil
df_test = df_test.loc[(df_test['match_id'] == 3857269) & (df_test['minute'] == 26)].head(1)
df_test.reset_index(drop=True, inplace=True)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams['mathtext.default'] = 'regular'

def point_on_line(start, end, distance=3):
    # Calculate the distance between the start and end points
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    line_length = (dx ** 2 + dy ** 2) ** 0.5

    # Calculate the unit vector of the line
    unit_dx = dx / line_length
    unit_dy = dy / line_length

    # Calculate the coordinates of the point 3 units away from the start point
    new_x = start[0] + unit_dx * distance
    new_y = start[1] + unit_dy * distance

    return (new_x, new_y)

# Define the coordinates of the three points
start = [df_test['x_coordinate'][0], df_test['y_coordinate'][0]]
end_l = [CONSTANTS.X_COORDINATE_POST_L, CONSTANTS.Y_COORDINATE_POST_L]
end_r = [CONSTANTS.X_COORDINATE_POST_R, CONSTANTS.Y_COORDINATE_POST_R]

#search points for arc
point_r = point_on_line(start, end_r)
point_l = point_on_line(start, end_l)

#add football field to plot
fig, ax = plt.subplots(figsize = (5, 10))
img = plt.imread("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Draw/background_pitch/102_120_18_62_penalty.png")
ax.imshow(img, alpha=0.8, extent=[102, 120, 18, 62])

#add angle lines
ax.plot([start[0], end_r[0]], [start[1], end_r[1]], '-o', label='connection: player - left post', color='gray')
ax.plot([start[0], end_l[0]], [start[1], end_l[1]], '-o', label='connection: player - right post', color='gray')
ax.plot(start[0], start[1], 'o', label='Vinicius Junior', color='red')

def draw_curve(p1, p2):
   a = (p2[1] - p1[1]) / (np.cosh(p2[0]) - np.cosh(p1[0]))
   b = p1[1] - a * np.cosh(p1[0])
   x = np.linspace(p1[0], p2[0], 100)
   y = a * np.cosh(x) + b
   return x, y

#add the angle circle
x, y = draw_curve(point_l, point_r)
text = str("{: .1f}".format(df_test['angle'][0]) + "°")
#ax.text((point_l[0]+point_r[0])/2-2.2, (point_l[1]+point_r[1])/2-0.2, text, fontsize=12)
ax.text(110,25, text, fontsize=12)
ax.plot(x, y, label=text, color='blue', linestyle='--')

ax.invert_yaxis()
ax.set_xlabel('x_coordinate')
ax.set_ylabel('y_coordinate')
ax.text(0.5, 1.02, "Angle Player to Goal \n Brazil - Switzerland, World Cup 2022, 26' 40''", ha='center', fontsize=12, transform=ax.transAxes)
legend = ax.legend(fontsize=10, loc='lower center')

#plt.tight_layout()
plt.show()