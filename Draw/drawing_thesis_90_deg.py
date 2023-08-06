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
img = plt.imread("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Draw/background_pitch/102_120_18_62_90_deg.png")
ax.imshow(img, alpha=0.8, extent=[18, 62, -120, -102])

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

x_teammates_to_plot = df_to_plot["y_coordinate"][(df_to_plot['teammate'] == True) & (df_to_plot["x_coordinate"] >= 100) ]
y_teammates_to_plot = -df_to_plot["x_coordinate"][(df_to_plot['teammate'] == True) & (df_to_plot["x_coordinate"] >= 100)]
x_opponents_to_plot = df_to_plot["y_coordinate"][(df_to_plot['teammate'] == False) & (df_to_plot["x_coordinate"] >= 100)]
y_opponents_to_plot = -df_to_plot["x_coordinate"][(df_to_plot['teammate'] == False) & (df_to_plot["x_coordinate"] >= 100) ]
x_GK = df_to_plot['y_coordinate'][(df_to_plot['name_position'] == "Goalkeeper") & (df_to_plot['teammate'] == False)].iloc[0]
y_GK = -df_to_plot['x_coordinate'][(df_to_plot['name_position'] == "Goalkeeper") & (df_to_plot['teammate'] == False)].iloc[0]


#plot all teammates
ax.plot(x_teammates_to_plot, y_teammates_to_plot, 'o', color='#F1DE1F', label="location Brazil")
#plot all opponents
ax.plot(x_opponents_to_plot, y_opponents_to_plot, 'o', color='red', label="location Switzerland")

#plot the most important points
#this is the player which initially took the shot
ax.plot(x_original, y_original, 'D', markeredgecolor='#3E32BA', markerfacecolor='#F1DE1F', label="location initial shot")
#this is the best alternative
ax.plot(x_alternative, y_alternative, '^', markeredgecolor='#3E32BA', markerfacecolor='#F1DE1F', label="location best alternative")
#this is the closest opponent
ax.plot(x_alt_opponent, y_alt_opponent, 'o', markeredgecolor='red', markerfacecolor='white', label="location closest defender")
#this is the location where the new shot will happen
ax.plot(x_ball, y_ball, 'o', markersize=6, markeredgecolor='black', markerfacecolor='none', label="location hypothetical shot")


# plot the labels
for i in range(len(x_original)):
    #add the name of the original player and its original xG value (show 2 decimal values)
    name = label_original[i]
    all_names = name.split()
    last_name = all_names[-1]
    text =  str("Vinicius Junior"+": " "{: .2f}".format(label_xG_original[i])+"xG")
    ax.text(x_original[i] + 0.3, y_original[i] +0.3,text, fontsize=12)
    #add the name of the alternative player
    name = label_alternative_player[i]
    all_names = name.split()

    ax.text(x_alternative[i] + 3, y_alternative[i] + 0.4, "Richarlison", fontsize=12)
    # add the name of the alternative opponent
    name = label_alternative_opponent[i]
    all_names = name.split()
    last_name = all_names[-1]
    #Akanji
    ax.text(x_alt_opponent[i] + 0.1, y_alt_opponent[i] +0.35, last_name, fontsize=12)
    #add the xG value of the new shooting position (show 2 decimal values)
    text = str("{: .2f}".format(label_xG_new_loca[i])+"xP*xG")
    #annotation of xG alternative
    ax.text(x_ball[i]-0.3 , y_ball[i] -0.3, text , fontsize=12)



# Connect the points with lines
for i in range(len(x_original)):
    #show the pass in the diagram
    arrow = FancyArrowPatch((x_original[i], y_original[i]), (x_ball[i], y_ball[i]), arrowstyle='->', linestyle='--', mutation_scale=10, color='black', label='xP, passing distance')
    ax.add_patch(arrow)
    dx = x_ball[i] - x_original[i]
    dy = y_ball[i] - y_original[i]
    text = str("{: .2f}".format(label_xPass[i])+"xP, "+ "{: .2f}".format(label_pass_distance[i]) + "m")
    # xp annotation and passing distance
    ax.annotate(text, xy=(34,-114), xytext=(-5, 5),
                textcoords='offset points', fontsize=12, ha='center')

    #show the run of the teammate in the diagram
    arrow = FancyArrowPatch((x_alternative[i], y_alternative[i]), (x_ball[i], y_ball[i]), arrowstyle='->',
                            mutation_scale=10, color='grey', label='run to hypothetical shot')
    dx = x_ball[i] - x_alternative[i]
    dy = y_ball[i] - y_alternative[i]
    ax.add_patch(arrow)
    text = str("{: .2f}".format(label_alternative_teammate_distance[i]) + "m")
    #distance alternative teammate
    ax.annotate(text, xy=(44.1,-114), xytext=(-5, 5),
                textcoords='offset points', fontsize=12, ha='center')

    #show the run of the opponent in the diagram
    arrow = FancyArrowPatch((x_alt_opponent[i], y_alt_opponent[i]), (x_ball[i], y_ball[i]), arrowstyle='->',
                            mutation_scale=10, color='grey', label='run')
    ax.add_patch(arrow)
    dx = x_ball[i] - x_alt_opponent[i]
    dy = y_ball[i] - y_alt_opponent[i]
    text = str("{: .2f}".format(label_alternative_opponent_distance[i]) + "m")
    #annotation of opponent, akanji distance
    ax.annotate(text, xy=(41.3,-112.5), xytext=(-5, 5),
                textcoords='offset points', fontsize=12, ha='center')


#plot the movement of the GK
x_intersection, y_intersection = DataManipulation.intersection_point_GK_Shot(goalkeeper=(-y_GK, x_GK), shot=(-y_shot, x_shot))
copy = x_intersection
x_intersection = y_intersection
y_intersection = -copy



#additionally we need to plot until which point the goalkeeper can run
def delta_coordinates(x1, y1, x2, y2, delta):
    # calculate slope of the line
    m = (y2 - y1) / (x2 - x1)

    # calculate distance between starting and endpoint
    d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # calculate horizontal and vertical leg lengths
    x = math.sqrt(delta**2 / (1 + m**2))
    y = abs(m * x)

    # calculate new point coordinates
    if m >= 0:
        x_new = x2 - x
        y_new = y2 - y
    else:
        x_new = x2 - x
        y_new = y2 - y

    return x_new, y_new

# Add a dashed line showing the optimal line
ax.plot([x_shot, CONSTANTS.Y_COORDINATE_GOALCENTRE], [y_shot,-CONSTANTS.X_COORDINATE_GOALCENTRE ], linestyle='dotted', color='lightgray', label="bisection hypothetical shot, goal centre")

x_GK_end, y_GK_end = delta_coordinates(x_GK, y_GK, x_intersection, y_intersection, delta=df_test['delta_GK_line_alternative'])
# Add the two points to the axis as scatter plots, with labels
ax.plot(x_GK, y_GK, 'o', color='blue', label=f"goalkeeper - start location: ({-y_GK}, {x_GK})")
text_x = str("{:.1f}".format(-y_GK_end))
text_y = str("{:.1f}".format(x_GK_end))
ax.plot(x_GK_end, y_GK_end, 's', markeredgecolor='lightgray', markerfacecolor='blue', label=f"goalkeeper - end location: ({text_x}, {text_y})")

#show the run of the opponent in the diagram
arrow = FancyArrowPatch((x_GK, y_GK), (x_GK_end, y_GK_end), arrowstyle='->',
                        mutation_scale=10, color='grey', label='run to hypothetical shot')
ax.add_patch(arrow)
text = "2.70m"
ax.annotate(text, xy=(37.1,-119.93), xytext=(-5, 5),
                textcoords='offset points', fontsize=12, ha='center')
#ax.plot(CONSTANTS.Y_COORDINATE_GOALCENTRE,-CONSTANTS.X_COORDINATE_GOALCENTRE , 'x', color='gray', label=f"goal centre: ({CONSTANTS.X_COORDINATE_GOALCENTRE}, {CONSTANTS.Y_COORDINATE_GOALCENTRE})")



# Set x and y axis labels
# Add legend
desired_order = ['goalkeeper - start location: (118.8, 37.3)', 'goalkeeper - end location: (120.0, 40.0)', 'bisection hypothetical shot, goal centre',
                 'location initial shot', 'xP, passing distance', 'location best alternative', 'location closest defender', 'run',
                 'location Brazil', 'location Switzerland',
                 'location hypothetical shot', 'goal centre: (120, 40)']

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
ax.set_title("Visualisation of the xG model and the decision quality", fontsize=12)

# Show the plot
plt.tight_layout()
plt.show()
