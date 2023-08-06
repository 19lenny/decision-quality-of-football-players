import matplotlib.pyplot as plt
from SetUp import CONSTANTS, JSONtoDF


df_test = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
#wm 22 switzerland vs brazil
df_test = df_test.loc[(df_test['match_id'] == 3857269) & (df_test['minute'] == 26)].head(1)
df_test.reset_index(drop=True, inplace=True)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams['mathtext.default'] = 'regular'

# Define the x and y coordinates of the two points
x1 = df_test['x_coordinate'][0]
y1 = df_test['y_coordinate'][0]
x2 = CONSTANTS.X_COORDINATE_GOALCENTRE
y2 = CONSTANTS.Y_COORDINATE_GOALCENTRE
x_GK = df_test

# Create a new figure and axis
fig, ax = plt.subplots(figsize = (5, 10))
img = plt.imread("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Draw/background_pitch/102_120_18_62_penalty.png")
ax.imshow(img, alpha=0.8, extent=[102, 120, 18, 62])

# Add the two points to the axis as scatter plots, with labels
ax.plot(x1, y1, 'o', color='red', label=f"Vinicius Junior: ({x1}, {y1})")
ax.plot(x2, y2, 'x', color='gray', label=f"Goal Centre: ({x2}, {y2})")

# Add a dashed line connecting the two points
ax.plot([x1, x2], [y1, y2], linestyle='--', color='blue', label="distance to goal centre")

# Add a label to the line showing the distance
text = str("{: .2f}".format(df_test['distance_to_goal_centre'][0] * 0.9144) + "m")
ax.text((x1+x2)/2, (y1+y2)/2, text, fontsize=12)

ax.invert_yaxis()
ax.set_xlabel('x_coordinate')
ax.set_ylabel('y_coordinate')
ax.text(0.5, 1.02, "Distance to Goal Centre \n Brazil - Switzerland, World Cup 2022, 26' 40''", ha='center', fontsize=12, transform=ax.transAxes)
legend = ax.legend(fontsize=10, loc='lower center')
#plt.tight_layout()
# Show the plot
plt.show()
