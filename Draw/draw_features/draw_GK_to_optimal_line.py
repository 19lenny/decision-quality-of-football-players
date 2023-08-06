import matplotlib.pyplot as plt
from SetUp import CONSTANTS, JSONtoDF, DataManipulation
from SetUp.DecisionEvaluation.evaluationHelper import getPlayersOfEvent

df_test = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
# wm 22 switzerland vs brazil
df_test = df_test.loc[(df_test['match_id'] == 3857269) & (df_test['minute'] == 26)].head(1)
df_test.reset_index(drop=True, inplace=True)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams['mathtext.default'] = 'regular'

# Define the x and y coordinates of the two points
shot_x = df_test['x_coordinate'][0]
shot_y = df_test['y_coordinate'][0]
x_GoalCentre = CONSTANTS.X_COORDINATE_GOALCENTRE
y_GoalCentre = CONSTANTS.Y_COORDINATE_GOALCENTRE

# get x,y of GK
df_to_plot = getPlayersOfEvent(df_test['shot_freeze_frame'][0], "drawing")

x_GK = df_to_plot['x_coordinate'][(df_to_plot['name_position'] == "Goalkeeper") & (df_to_plot['teammate'] == False)].iloc[0]
y_GK = df_to_plot['y_coordinate'][(df_to_plot['name_position'] == "Goalkeeper") & (df_to_plot['teammate'] == False)].iloc[0]
x_intersection, y_intersection = DataManipulation.intersection_point_GK_Shot(goalkeeper=(x_GK, y_GK), shot=(shot_x, shot_y))
# create a new figure and axis
fig, ax = plt.subplots(figsize = (5, 10))
img = plt.imread("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Draw/background_pitch/102_120_18_62_penalty.png")
ax.imshow(img, alpha=0.8, extent=[102, 120, 18, 62])

# add the two points to the axis as scatter plots, with labels
ax.plot(shot_x, shot_y, 'o', color='red', label=f"Vinicius Junior: ({shot_x}, {shot_y})")
ax.plot(x_GK, y_GK, 'o', color='blue', label=f"Yann Sommer: ({x_GK}, {y_GK})")
ax.plot(CONSTANTS.X_COORDINATE_GOALCENTRE, CONSTANTS.Y_COORDINATE_GOALCENTRE, 'x', color='gray', label=f"Goal Centre: ({CONSTANTS.X_COORDINATE_GOALCENTRE}, {CONSTANTS.Y_COORDINATE_GOALCENTRE})")

# add a line connecting the two points
ax.plot([shot_x, CONSTANTS.X_COORDINATE_GOALCENTRE], [shot_y, CONSTANTS.Y_COORDINATE_GOALCENTRE], linestyle='--', color='gray', label="distance to goal centre")
ax.plot([x_GK, x_intersection], [y_GK, y_intersection], linestyle='--', color='blue', label="distance GK to optimal line (1.3m)")

text = str("{: .2f}".format(df_test['delta_distance_GK_to_optimal_line'][0] * 0.9144) + "m")
ax.text(x_intersection-2, y_intersection+1.2, text, fontsize=12)

ax.invert_yaxis()
ax.set_xlabel('x_coordinate')
ax.set_ylabel('y_coordinate')
ax.text(0.5, 1.02, "Delta GK to Optimal Line \n Brazil - Switzerland, World Cup 2022, 26' 40''", ha='center', fontsize=12, transform=ax.transAxes)
legend = ax.legend(fontsize=10, loc='lower center')
#plt.tight_layout()
# Show the plot
plt.show()
