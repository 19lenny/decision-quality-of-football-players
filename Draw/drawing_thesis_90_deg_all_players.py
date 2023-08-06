import math

import matplotlib
import matplotlib.pyplot as plt
from SetUp import CONSTANTS, JSONtoDF, DataManipulation
from matplotlib.patches import FancyArrowPatch

from SetUp.DecisionEvaluation.evaluationHelper import getPlayersOfEvent


df_test = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)

#wm 22 switzerland vs brazil
df_test = df_test.loc[(df_test['match_id'] == 3857269) & (df_test['minute'] == 26)].head(1)
df_test.reset_index(drop=True, inplace=True)

# x and y coordinates of the points to be plotted
# all points needs to be transformed clockwise, such that they fit in the thesis
x_original = df_test['y_coordinate']
y_original = -df_test['x_coordinate']
x_alternative = df_test['y_best_alt']
y_alternative = -df_test['x_best_alt']
x_alt_opponent = df_test['y_opponent']
y_alt_opponent = -df_test['x_opponent']
x_ball = df_test['y_ball']
y_ball = -df_test['x_ball']
x_shot = df_test['y_ball'][0]
y_shot = -df_test['x_ball'][0]

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams['mathtext.default'] = 'regular'

# create a new figure and axis
fig, ax = plt.subplots(figsize=(12,8))
img = plt.imread("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Draw/background_pitch/72_120_0_80_penalty40_90deg.png")
ax.imshow(img, alpha=0.8, extent=[0, 80, -120, -72])

#labels for the points
#passing player
label_original = df_test['player']
label_xG_original = df_test['xG']
#shooting player
label_alternative_player = df_test['player_name_alt']
label_alternative_opponent = df_test['player_namer_opponent']
#distance from the teammate to the shooting location,
#*0.9144 is there to convert from yards to meter
label_alternative_teammate_distance = df_test['distance_teammember'] * 0.9144
label_alternative_opponent_distance = df_test['distance_opponent'] * 0.9144
label_pass_distance = df_test['distance_ball'] * 0.9144
#xG from new location
label_xG_new_loca = df_test['xG_best_alternative']
#line values are the xP values
label_xPass = df_test['xP_best_alternative']

#get all the opponents and other teammembers, only plot the players that are within the penalty box, for better visability
df_to_plot = getPlayersOfEvent(df_test['shot_freeze_frame'][0], "drawing")

x_teammates_to_plot = df_to_plot["y_coordinate"][(df_to_plot['teammate'] == True) ]
y_teammates_to_plot = -df_to_plot["x_coordinate"][(df_to_plot['teammate'] == True)]
x_opponents_to_plot = df_to_plot["y_coordinate"][(df_to_plot['teammate'] == False) ]
y_opponents_to_plot = -df_to_plot["x_coordinate"][(df_to_plot['teammate'] == False) ]
x_GK = df_to_plot['y_coordinate'][(df_to_plot['name_position'] == "Goalkeeper") & (df_to_plot['teammate'] == False)].iloc[0]
y_GK = -df_to_plot['x_coordinate'][(df_to_plot['name_position'] == "Goalkeeper") & (df_to_plot['teammate'] == False)].iloc[0]


#plot all teammates
ax.plot(x_teammates_to_plot, y_teammates_to_plot, 'o', color='#F1DE1F', label="locations Brazil")
#plot all opponents
ax.plot(x_opponents_to_plot, y_opponents_to_plot, 'o', color='red', label="locations Switzerland")

#plot the most important points
#this is the player which initially took the shot
ax.plot(x_original, y_original, 'D', markeredgecolor='#3E32BA', markerfacecolor='#F1DE1F', label="location initial shot")



# Add the two points to the axis as scatter plots, with labels
ax.plot(x_GK, y_GK, 'o', color='blue', label=f"goalkeeper Switzerland")



ax.plot(CONSTANTS.Y_COORDINATE_GOALCENTRE,-CONSTANTS.X_COORDINATE_GOALCENTRE , 'x', color='gray', label=f"goal centre")



# Set x and y axis labels
# Add legend
desired_order = ['goal centre','location initial shot', 'locations Brazil', 'goalkeeper Switzerland', 'locations Switzerland']

# get the legend
handles, labels = ax.get_legend_handles_labels()


sorted_handles = []
sorted_labels = []
for label in desired_order:
    if label in labels:
        index = labels.index(label)
        sorted_handles.append(handles[index])
        sorted_labels.append(labels[index])


legend = ax.legend(sorted_handles, sorted_labels, loc='upper right', ncol=1, prop={'size': 10}, markerscale=0.8, bbox_to_anchor=(1, 0.93))

ax.invert_xaxis()
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)
ax.set_title("Visualisation of the freeze-frame: Brazil - Switzerland, 26' 40'', WC 22", fontsize=12)

# Show the plot
plt.tight_layout()
plt.show()
