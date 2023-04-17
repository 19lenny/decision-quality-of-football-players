from scipy.stats import stats

from SetUp import JSONtoDF, CONSTANTS
import numpy as np

# Plotting
import matplotlib.pyplot as plt
from Draw import FCPython
import pandas as pd
# Statistical fitting of models
import statsmodels.api as sm
import statsmodels.formula.api as smf

shots_model = pd.concat([JSONtoDF.createDF(CONSTANTS.JSONTRAINSHOTS), JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)])

#dataframe where all the shots happened
shots_model = shots_model[['goal', 'x_coordinate', 'y_coordinate', 'angle',
                           'angleInRadian', 'distance_to_goal_centre', 'shot_statsbomb_xg']]

x = shots_model['x_coordinate']
y = shots_model['y_coordinate']

# dataframe where only the goals happened
goals_only = shots_model[shots_model['goal'] == 1]
x_goals_only = goals_only['x_coordinate']
y_goals_only = goals_only['y_coordinate']

# Two dimensional histogram for goal and shot visualization
H_Shot = np.histogram2d(shots_model['x_coordinate'], shots_model['y_coordinate'], bins=50)
goals_only = shots_model[shots_model['goal'] == 1]

H_Goal = np.histogram2d(goals_only['x_coordinate'], goals_only['y_coordinate'], bins=50)

# Plot the number of shots from different points
# histogram where how many shots happened
fig, ax = FCPython.createGoalMouth()
histogram = ax.hist2d(x, y, bins=(50, 50))
pos = ax.imshow(histogram[0], aspect='auto')
fig.colorbar(pos, ax=ax)
ax.invert_yaxis()
ax.set_xlabel('x_coordinate')
ax.set_ylabel('y_coordinate')
ax.set_title('Number of shots')
#fig.gca().set_aspect('equal', adjustable='box')
fig.tight_layout()
plt.show()

# Plot the number of GOALS from different points
# histogram where and how many goals happened
#todo change away from create goal mouth, instead put image in background
#todo use same color as the other histograms
fig, ax = FCPython.createGoalMouth()
histogram = ax.hist2d(x_goals_only, y_goals_only, bins=(25, 25))
pos = ax.imshow(histogram[0], aspect='auto')
fig.colorbar(pos, ax=ax)
ax.invert_yaxis()
ax.set_xlabel('x_coordinate')
ax.set_ylabel('y_coordinate')
ax.set_title('Number of goals')
#fig.gca().set_aspect('equal', adjustable='box')
fig.tight_layout()
plt.show()

# Get first 5000 shots
shots_500 = shots_model.iloc[:500]

# Plot first 500 shots goal angle and checks whether it was a goal or not
# it creates a binary figure to see the distribution of goals with respect to the angle
fig, ax = plt.subplots(num=1)
ax.plot(shots_500['angleInRadian'] * 180 / np.pi, shots_500['goal'], linestyle='none', marker='.', color='black')
ax.set_ylabel('Goal scored')
# in degree since above is the transformation from in radian to in degree
ax.set_xlabel("Shot angle (degree)")
ax.set_title("the scoring outcome in dependence of the angle for 500 shots")
plt.ylim((-0.05, 1.05))
ax.set_yticks([0, 1])
ax.set_yticklabels(['0', '1'])
plt.show()

# Show empirically how goal angle predicts probability of scoring
# probability is just number of goals / number of shots in this angle area
shotcount_dist = np.histogram(shots_model['angleInRadian'] * 180 / np.pi, bins=40, range=[0, 179])
goalcount_dist = np.histogram(goals_only['angleInRadian'] * 180 / np.pi, bins=40, range=[0, 179])
prob_goal = np.divide(goalcount_dist[0], shotcount_dist[0])
angle = shotcount_dist[1]
midangle = (angle[:-1] + angle[1:]) / 2
fig, ax = plt.subplots(num=2)
ax.plot(midangle, prob_goal, linestyle='none', marker='.', color='black')
ax.set_ylabel('Probability chance scored')
ax.set_xlabel("Shot angle (degrees)")
ax.set_title("number of goals divided by number of shot depending on the angle")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()

# Make single variable model of angle
# Using logistic regression we find the optimal values of b
# This process minimizes the loglikelihood
test_model = smf.glm(formula="goal ~ angleInRadian", data=shots_model,
                     family=sm.families.Binomial()).fit()
b = test_model.params

# plot probability of scoring according to angle
# since it calculates expected misses
xGprob = 1 - 1 / (1 + np.exp(b[0] + b[1] * midangle * np.pi / 180))
fig, ax = plt.subplots(num=1)
ax.plot(midangle, prob_goal, linestyle='none', marker='.', color='red')
ax.plot(midangle, xGprob, linestyle='solid', color='black')
ax.set_ylabel('Probability chance scored')
ax.set_xlabel("Shot angle (degrees)")
ax.set_title("real scoring chance vs. calculated scoring chance (only angle)")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()

####### distance

# Show empirically how distance predicts probability of scoring
shotcount_dist = np.histogram(shots_model['distance_to_goal_centre'], bins=40, range=[0, 70])
goalcount_dist = np.histogram(goals_only['distance_to_goal_centre'], bins=40, range=[0, 70])
prob_goal = np.divide(goalcount_dist[0], shotcount_dist[0])
distance = shotcount_dist[1]

middistance = (distance[:-1] + distance[1:]) / 2
fig, ax = plt.subplots(num=2)
ax.plot(middistance, prob_goal, linestyle='none', marker='.', color='black')
ax.set_ylabel('Probability chance scored')
ax.set_xlabel("Shot distance (yards)")
ax.set_title("number of goals divided by number of shot depending on the distance")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Make single variable model of distance
test_model = smf.glm(formula="goal ~ distance_to_goal_centre", data=shots_model,
                     family=sm.families.Binomial()).fit()

b = test_model.params
# since it calculates expected misses
y = 1 - 1 / (1 + np.exp(b[0] + b[1] * middistance))
ax.plot(middistance, y, linestyle='solid', color='grey')

plt.show()
"""
# A general model for fitting goal probability
# List the model variables you want here
model_variables = ['angleInRadian', 'distance_to_goal_centre']
model = ''
for v in model_variables[:-1]:
    model = model + v + ' + '
model = model + model_variables[-1]
# Fit the model
test_model = smf.glm(formula="goal ~ " + model, data=shots_model,
                     family=sm.families.Binomial()).fit()

b = test_model.params


# Return xG value for more general model
def calculate_xG(sh):
    bsum = b[0]
    for i, v in enumerate(model_variables):
        bsum = bsum + b[i + 1] * sh[v]
    xG = 1 / (1 + np.exp(bsum))
    return xG


# Add an xG to my dataframe
# 1- since our wxG calculates expected miss
xG = 1 - shots_model.apply(calculate_xG, axis=1)
shots_model = shots_model.assign(xG=xG)

xReal = shots_model[model_variables]
xGG =  test_model.predict(xReal)
shots_model["xGG"] = xGG

#goal for later draw a card of goal scoring probability with angle and distance
"""