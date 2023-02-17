import numpy as np
import statsmodels.api as sm
from SetUp import JSONtoDF


def create_model(filename):
    # achtung modell kreiert kein intercept, dies muss bei der Arbeit genauer angesehen werden
    # https://www.statsmodels.org/dev/generated/statsmodels.discrete.discrete_model.Logit.html
    # getting the df
    # https://towardsdatascience.com/building-a-logistic-regression-in-python-step-by-step-becd4d56c9c8
    df = JSONtoDF.createDF(filename)

    print(df.info())

    # train the model
    X_train = df[["distance_to_goal_centre", "angle"]]
    y_train = df[['goal']]
    log_reg = sm.Logit(y_train, X_train).fit()

    # return the model
    return log_reg


def show_info(regression):
    print(regression.summary2())


def prediction(modelname, regression, filename, attributes):
    df = JSONtoDF.createDF(filename)
    xReal = df[attributes]
    xGoal = regression.predict(xReal)
    df[modelname] = xGoal
    return df


def calculateAccuracy(modelname, df):

    nameOfColumn = "differenceInPcOf" + modelname
    df[nameOfColumn] = df[modelname] * 100 / df["shot_statsbomb_xg"]
    print("the mean of the difference in percentage of ", modelname, " is: ", df[nameOfColumn].mean())
    return df
