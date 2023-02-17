import statsmodels.formula.api as smf
from matplotlib import colors, cm

from SetUp import JSONtoDF
import numpy as np
import pandas as pd

# Plotting
import matplotlib.pyplot as plt
import FCPython

# Statistical fitting of models
import statsmodels.api as sm
import statsmodels.formula.api as smf

shots_model = JSONtoDF.createDF("../JSON/allModelData.json")
shots_model = shots_model[['goal', 'x_coordinate', 'y_coordinate']]
x_coord = shots_model['x_coordinate']

shots_model = JSONtoDF.createDF("../JSON/allModelData.json")
shots_model = shots_model[['goal', 'x_coordinate', 'y_coordinate', 'angle', 'distance_to_goal_centre']]
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


fig, ax = FCPython.createGoalMouth()
histogram = ax.hist2d(x, y, bins=(60, 60))
pos = ax.imshow(histogram[0], aspect='auto')
fig.colorbar(pos, ax=ax)
ax.set_title('Number of shots')
# fig.gca().set_aspect('equal', adjustable='box')
fig.tight_layout()
plt.show()

# Plot the number of GOALS from different points
fig, ax = FCPython.createGoalMouth()
histogram = ax.hist2d(x_goals_only, y_goals_only, bins=(20, 20))
pos = ax.imshow(histogram[0], aspect='auto')
fig.colorbar(pos, ax=ax)
ax.set_title('Number of goals')
# fig.gca().set_aspect('equal', adjustable='box')
fig.tight_layout()
plt.show()

# Plot a logistic curve
b = [3, -3]
x = np.arange(5, step=0.1)
y = 1 / (1 + np.exp(-b[0] - b[1] * x))
fig, ax = plt.subplots(num=1)
plt.ylim((-0.05, 1.05))
plt.xlim((0, 5))
ax.set_ylabel('y')
ax.set_xlabel("x")
ax.plot(x, y, linestyle='solid', color='black')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()

# Get first 200 shots
shots_200 = shots_model.iloc[:5000]

# Plot first 200 shots goal angle
fig, ax = plt.subplots(num=1)
ax.plot(shots_200['angle'], shots_200['goal'], linestyle='none', marker='.', color='black')
ax.set_ylabel('Goal scored')
ax.set_xlabel("Shot angle (degrees)")
plt.ylim((-0.05, 1.05))
ax.set_yticks([0, 1])
ax.set_yticklabels(['No', 'Yes'])
plt.show()

# Show empirically how goal angle predicts probability of scoring
shotcount_dist = np.histogram(shots_model['angle'], bins=60, range=[0, 179])
goalcount_dist = np.histogram(goals_only['angle'], bins=60, range=[0, 179])
prob_goal = np.divide(goalcount_dist[0], shotcount_dist[0])
angle = shotcount_dist[1]
midangle = (angle[:-1] + angle[1:]) / 2
fig, ax = plt.subplots(num=2)
ax.plot(midangle, prob_goal, linestyle='none', marker='.', color='black')
ax.set_ylabel('Probability chance scored')
ax.set_xlabel("Shot angle (degrees)")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Now try sigmoid model
# This is a good model but NOT a good way of fitting.
# because each point contains lots of data points
b = [3, -3]
x = np.arange(179, step=0.1)
y = 1 / (1 + np.exp(b[0] + b[1] * x * np.pi / 180))
ax.plot(x, y, linestyle='solid', color='grey')
plt.show()

# Make single variable model of angle
# Using logistic regression we find the optimal values of b
# This process minimizes the loglikelihood
test_model = smf.glm(formula="goal ~ angle", data=shots_model,
                     family=sm.families.Binomial()).fit()
print(test_model.summary())
b = test_model.params

xGprob = 1 / (1 + np.exp(b[0] + b[1] * midangle))
fig, ax = plt.subplots(num=1)
ax.plot(midangle, prob_goal, linestyle='none', marker='.', color='black')
ax.plot(midangle, xGprob, linestyle='solid', color='black')
ax.set_ylabel('Probability chance scored!')
ax.set_xlabel("Shot angle (degrees)")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()
