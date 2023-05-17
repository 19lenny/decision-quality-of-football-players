import math

import matplotlib.pyplot as plt
from SetUp import CONSTANTS, JSONtoDF, DataManipulation
from matplotlib.patches import FancyArrowPatch

from SetUp.DecisionEvaluation.evaluationHelper import getPlayersOfEvent

#todo: save the picture and decide on one shot
df_test = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
#wm 22 switzerland vs brazil
#df_test = df_test.loc[(df_test['match_id'] == 3857269) & (df_test['minute'] == 26)].head(1)
df_test = df_test.loc[(df_test['match_id'] == 3857293) & (df_test['minute'] == 22)].head(1)
df_test.reset_index(drop=True, inplace=True)
# x and y coordinates of the points to be plotted
x_original = df_test['x_coordinate']
y_original = df_test['y_coordinate']
x_alternative = df_test['x_best_alt']
y_alternative = df_test['y_best_alt']
x_alt_opponent = df_test['x_opponent']
y_alt_opponent = df_test['y_opponent']
x_ball = df_test['x_ball']
y_ball = df_test['y_ball']
x_shot = df_test['x_ball'][0]
y_shot = df_test['y_ball'][0]

# Create a new figure and axis
fig, ax = plt.subplots(figsize=(7,10))
img = plt.imread("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Draw/background_pitch/95_120_09_71_bigpenalty.png")
ax.imshow(img, alpha=0.8, extent=[95, 120, 9, 71])

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
x_teammates_to_plot = df_to_plot["x_coordinate"][(df_to_plot['teammate'] == True) ]
y_teammates_to_plot = df_to_plot["y_coordinate"][(df_to_plot['teammate'] == True) ]
x_opponents_to_plot = df_to_plot["x_coordinate"][(df_to_plot['teammate'] == False) ]
y_opponents_to_plot = df_to_plot["y_coordinate"][(df_to_plot['teammate'] == False) ]
x_GK = df_to_plot['x_coordinate'][(df_to_plot['name_position'] == "Goalkeeper") & (df_to_plot['teammate'] == False)].iloc[0]
y_GK = df_to_plot['y_coordinate'][(df_to_plot['name_position'] == "Goalkeeper") & (df_to_plot['teammate'] == False)].iloc[0]


#plot all teammates
ax.plot(x_teammates_to_plot, y_teammates_to_plot, 'o', color='#89CFF0', label="location teammate")
#plot all opponents
ax.plot(x_opponents_to_plot, y_opponents_to_plot, 'o', color='#FF6961', label="location opponent")

#plot the most important points
#this is the player which initially took the shot
ax.plot(x_original, y_original, 'o', color='black', label="location player")
#this is the best alternative
ax.plot(x_alternative, y_alternative, 'o', color='blue', label="location best teammate")
#this is the closest opponent
ax.plot(x_alt_opponent, y_alt_opponent, 'o', color='red', label="location best opponent")
#this is the location where the new shot will happen
ax.plot(x_ball, y_ball, 'o', markersize=6, markeredgecolor='black', markerfacecolor='none', label="shot position")


# plot the labels
for i in range(len(x_original)):
    #add the name of the original player and its original xG value (show 2 decimal values)
    name = label_original[i]
    all_names = name.split()
    last_name = all_names[-1]
    text =  str(last_name+": " "{: .2f}".format(label_xG_original[i])+"xG")
    ax.text(x_original[i] + 0.3, y_original[i] + 0.1,text, fontsize=8)
    #add the name of the alternative player
    name = label_alternative_player[i]
    all_names = name.split()
    last_name = all_names[-1]
    ax.text(x_alternative[i] + 0.1, y_alternative[i] + 0.1, last_name, fontsize=8)
    #ax.text(x_alternative[i] + 0.3, y_alternative[i] + 0.2, "Richarlison", fontsize=8)
    # add the name of the alternative opponent
    name = label_alternative_opponent[i]
    all_names = name.split()
    last_name = all_names[-1]
    ax.text(x_alt_opponent[i] + 0.1, y_alt_opponent[i] + 0.1, last_name, fontsize=8)
    #add the xG value of the new shooting position (show 2 decimal values)
    text = str("{: .2f}".format(label_xG_new_loca[i])+"xP*xG")
    ax.text(x_ball[i] + 0.1, y_ball[i] + 0.1, text , fontsize=8)



# Connect the points with lines
for i in range(len(x_original)):
    #show the pass in the diagram
    arrow = FancyArrowPatch((x_original[i], y_original[i]), (x_ball[i], y_ball[i]), arrowstyle='->', linestyle='dotted', mutation_scale=10, color='grey', label='pass, xP')
    ax.add_patch(arrow)
    dx = x_ball[i] - x_original[i]
    dy = y_ball[i] - y_original[i]
    text = str("{: .2f}".format(label_xPass[i])+"xP, "+ "{: .2f}".format(label_pass_distance[i]) + "m")
    ax.annotate(text, xy=(x_original[i] + dx / 2, y_original[i] + dy / 2), xytext=(-5, 5),
                textcoords='offset points', fontsize=8, ha='center')

    #show the run of the teammate in the diagram
    arrow = FancyArrowPatch((x_alternative[i], y_alternative[i]), (x_ball[i], y_ball[i]), arrowstyle='->',
                            mutation_scale=10, color='grey', label='run, distance')
    dx = x_ball[i] - x_alternative[i]
    dy = y_ball[i] - y_alternative[i]
    ax.add_patch(arrow)
    text = str("{: .2f}".format(label_alternative_teammate_distance[i]) + "m")
    ax.annotate(text, xy=(0.4+x_alternative[i] + dx / 2, 0.7+y_alternative[i] + dy / 2), xytext=(-5, 5),
                textcoords='offset points', fontsize=8, ha='center')

    #show the run of the opponent in the diagram
    arrow = FancyArrowPatch((x_alt_opponent[i], y_alt_opponent[i]), (x_ball[i], y_ball[i]), arrowstyle='->',
                            mutation_scale=10, color='grey', label='run, distance')
    ax.add_patch(arrow)
    dx = x_ball[i] - x_alt_opponent[i]
    dy = y_ball[i] - y_alt_opponent[i]
    text = str("{: .2f}".format(label_alternative_opponent_distance[i]) + "m")
    ax.annotate(text, xy=(x_alt_opponent[i] + dx / 2, y_alt_opponent[i] + dy / 2), xytext=(-5, 5),
                textcoords='offset points', fontsize=8, ha='center')


#plot the movement of the GK
x_intersection, y_intersection = DataManipulation.intersection_point_GK_Shot(goalkeeper=(x_GK, y_GK), shot=(x_shot, y_shot))

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

x_GK_end, y_GK_end = delta_coordinates(x_GK, y_GK, x_intersection, y_intersection, delta=df_test['delta_GK_to_optimal_line'])
# Add the two points to the axis as scatter plots, with labels
ax.plot(x_GK, y_GK, 'o', color='orange', label=f"goalkeeper Zigi - starting location: ({x_GK}, {y_GK})")
text_x = str("{:.1f}".format(x_GK_end))
text_y = str("{:.1f}".format(y_GK_end))
ax.plot(x_GK_end, y_GK_end, 'o', color='orange', label=f"goalkeeper Zigi - end location: ({text_x}, {text_y})")
#show the run of the opponent in the diagram
arrow = FancyArrowPatch((x_GK_end, y_GK_end), (x_intersection, y_intersection), arrowstyle='->',
                        mutation_scale=10, color='red', label='delta GK to optimal line')
ax.add_patch(arrow)


#show the run of the opponent in the diagram
arrow = FancyArrowPatch((x_GK, y_GK), (x_GK_end, y_GK_end), arrowstyle='->',
                        mutation_scale=10, color='grey', label='run, distance')
ax.add_patch(arrow)
ax.plot(CONSTANTS.X_COORDINATE_GOALCENTRE, CONSTANTS.Y_COORDINATE_GOALCENTRE, 'x', color='gray', label=f"Goal Centre: ({CONSTANTS.X_COORDINATE_GOALCENTRE}, {CONSTANTS.Y_COORDINATE_GOALCENTRE})")

# Add a dashed line showing the optimal line
ax.plot([x_shot, CONSTANTS.X_COORDINATE_GOALCENTRE], [y_shot, CONSTANTS.Y_COORDINATE_GOALCENTRE], linestyle='--', color='gray', label="defense line GK")



# Add a label to the line showing the distance
GK_to_line = DataManipulation.distanceObjectToPoint(x_GK_end, y_GK_end, x_intersection, y_intersection)
text = str("{: .2f}".format(GK_to_line * 0.9144) + "m")
ax.text(x_intersection-1.8, y_intersection-1.25, text, fontsize=8)


# Set x and y axis labels
# Add legend
handles, labels = ax.get_legend_handles_labels()
unique_labels = list(set(labels))
handles = [handles[labels.index(label)] for label in unique_labels]
legend = ax.legend(handles, unique_labels, loc='lower center', ncol=1, prop={'size': 7}, markerscale=0.8)

ax.invert_yaxis()
ax.set_xlabel('x_coordinate')
ax.set_ylabel('y_coordinate')
ax.set_title("Decision Visualization")

# Show the plot
plt.tight_layout()
plt.show()
