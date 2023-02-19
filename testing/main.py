import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
from Model import model
from SetUp import JSONtoDF


# first we have to create a model on all Shot Data (except the one we are evaluating)
logRegModel = model.create_model_glm(
    "/JSON/allModelData.json")

# next step is to show the info of the model
model.show_info(logRegModel)

# next step is to predict the probability of each shot of the EM2020 and WM2022
# the prediction should be saved to the dataframe and added to the json file

# test of Angle and Distance
modelname = "xGAngleDistance"
attributes = ['angle', 'distance_to_goal_centre']

# EM 2020
dfEM2020 = model.prediction(modelname, logRegModel,
                            '/JSON/ShotsEM2020.json', attributes)
dfEM2020 = model.calculateAccuracy(modelname, dfEM2020)

#model2
df = JSONtoDF.createDF("../JSON/allModelData.json")


# train the model
X_train = df[["distance_to_goal_centre", "angle"]]
y_train = df[['goal']]
logreg = LogisticRegression()
logreg.fit(X_train, y_train)

#em
dfEM = JSONtoDF.createDF("../JSON/ShotsEM2020.json")
X_test = dfEM[["distance_to_goal_centre", "angle"]]
y_pred = logreg.predict_proba(X_test)
#print(y_pred[:,0])
dfEM["EstimatedXGModel2"] = y_pred[:,0]
y_test = dfEM['goal']
print(logreg.intercept_, logreg.coef_, logreg.score(X_test, y_test))
print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))

dfEM = dfEM[['angle', 'distance_to_goal_centre', 'EstimatedXGModel2', "xGAngleDistance", 'shot_statsbomb_xg', 'goal']]

