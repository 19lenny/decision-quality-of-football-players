import statsmodels.formula.api as smf
from matplotlib import colors, cm

from SetUp import JSONtoDF, DataManipulation
import numpy as np
import pandas as pd

# Plotting
import matplotlib.pyplot as plt
import FCPython

# Statistical fitting of models
import statsmodels.api as sm
import statsmodels.formula.api as smf

shots_model = JSONtoDF.createDF("../JSON/allModelData.json")

x_coord = shots_model['x_coordinate']

shots_model = JSONtoDF.createDF("../JSON/allModelData.json")

shots_model = shots_model[['goal', 'x_coordinate', 'y_coordinate', 'angle', 'angleInRadian', 'distance_to_goal_centre', 'shot_statsbomb_xg']]
x = shots_model['x_coordinate']
y = shots_model['y_coordinate']

goals_only = shots_model[shots_model['goal'] == 1]
x_goals_only = goals_only['x_coordinate']
y_goals_only = goals_only['y_coordinate']

# Two dimensional histogram
H_Shot = np.histogram2d(shots_model['x_coordinate'], shots_model['y_coordinate'], bins=50)
goals_only = shots_model[shots_model['goal'] == 1]
print(len(goals_only['goal']))
H_Goal = np.histogram2d(goals_only['x_coordinate'], goals_only['y_coordinate'], bins=50)

# Plot the number of shots from different points
# histogram number of shots
fig, ax = FCPython.createGoalMouth()
histogram = ax.hist2d(x, y, bins=(60, 60))
pos = ax.imshow(histogram[0], aspect='auto')
fig.colorbar(pos, ax=ax)
ax.set_title('Number of shots')
# fig.gca().set_aspect('equal', adjustable='box')
fig.tight_layout()
plt.show()

# Plot the number of GOALS from different points
# histogram number of goals
fig, ax = FCPython.createGoalMouth()
histogram = ax.hist2d(x_goals_only, y_goals_only, bins=(20, 20))
pos = ax.imshow(histogram[0], aspect='auto')
fig.colorbar(pos, ax=ax)
ax.set_title('Number of goals')
# fig.gca().set_aspect('equal', adjustable='box')
fig.tight_layout()
plt.show()

# Get first 5000 shots
shots_5000 = shots_model.iloc[:500]

# Plot first 500 shots goal angle
# yes no figure
fig, ax = plt.subplots(num=1)
ax.plot(shots_5000['angleInRadian'] * 180 / np.pi, shots_5000['goal'], linestyle='none', marker='.', color='black')
ax.set_ylabel('Goal scored')
ax.set_xlabel("Shot angle (degrees)")
plt.ylim((-0.05, 1.05))
ax.set_yticks([0, 1])
ax.set_yticklabels(['No', 'Yes'])
plt.show()

# Show empirically how goal angle predicts probability of scoring
shotcount_dist = np.histogram(shots_model['angleInRadian'] * 180 / np.pi, bins=60, range=[0, 179])
goalcount_dist = np.histogram(goals_only['angleInRadian'] * 180 / np.pi, bins=60, range=[0, 179])
prob_goal = np.divide(goalcount_dist[0], shotcount_dist[0])
angle = shotcount_dist[1]
midangle = (angle[:-1] + angle[1:]) / 2
fig, ax = plt.subplots(num=2)
ax.plot(midangle, prob_goal, linestyle='none', marker='.', color='black')
ax.set_ylabel('Probability chance scored')
ax.set_xlabel("Shot angle (degrees)")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()

# Make single variable model of angle
# Using logistic regression we find the optimal values of b
# This process minimizes the loglikelihood
test_model = smf.glm(formula="goal ~ angleInRadian", data=shots_model,
                     family=sm.families.Binomial()).fit()
print(test_model.summary())
b = test_model.params

# plot probability of scoring according to angle
print(midangle)
# since it calculates expected misses
xGprob = 1 - 1 / (1 + np.exp(b[0] + b[1] * midangle * np.pi / 180))
fig, ax = plt.subplots(num=1)
ax.plot(midangle, prob_goal, linestyle='none', marker='.', color='red')
ax.plot(midangle, xGprob, linestyle='solid', color='black')
ax.set_ylabel('Probability chance scored!')
ax.set_xlabel("Shot angle (degrees)")
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
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Make single variable model of distance
test_model = smf.glm(formula="goal ~ distance_to_goal_centre", data=shots_model,
                     family=sm.families.Binomial()).fit()
print(test_model.summary())
b = test_model.params
# since it calculates expected misses
y = 1 - 1 / (1 + np.exp(b[0] + b[1] * middistance))
ax.plot(middistance, y, linestyle='solid', color='grey')

plt.show()

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
print(test_model.summary())
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