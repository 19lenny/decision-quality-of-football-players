
import statsmodels.api as sm
import statsmodels.formula.api as smf
from SetUp import JSONtoDF
import pandas as pd


# sources
# https://towardsdatascience.com/building-a-logistic-regression-in-python-step-by-step-becd4d56c9c8
# https://www.youtube.com/watch?v=wHOgINJ5g54

# create a logistic regression without an intercept
# filename is the file location for which a model should be created, the file has to be in json format
# attributes are the attributes that the model should learn on (x_values)
def create_model_logit(filename, attributes):
    # creating the pandas data frame from the json file
    df = JSONtoDF.createDF(filename)
    # drop null values for better model quality
    df = df.dropna()
    # train the model based on the attributes
    X_train = df[attributes]
    y_train = df[['goal']]
    log_reg = sm.Logit(y_train, X_train).fit()

    # return the model
    return log_reg


# create a logistic regression with an intercept
# filename is the filelocation for which a model should be created, the file has to be in json format
# attributes are the attributes that the model should learn on (x_values)
def create_model_glm(filename, attributes):
    # create a pandas dataframe from the json file
    df = JSONtoDF.createDF(filename)

    # drop possible null values, the model gets more accurate
    df = df.dropna()

    # create the model based on the attributes
    model = ''
    for v in attributes[:-1]:
        model = model + v + ' + '
    model = model + attributes[-1]
    # Fit the model
    # the model is based on the binary y value 'goal',
    # the model gives the values for expected misses
    # this is corrected automatically in the prediction, where the whole thing is changed to expected goals
    test_model = smf.glm(formula="goal ~ " + model, data=df,
                         family=sm.families.Binomial()).fit()
    # return the model
    return test_model


# this method prints the information about a given regression
def show_info(regression):
    print(regression.summary())


# this method predicts the the xG with the help of a given model
# the prediction explicitely predicts xG and NOT xMisses
# the predictions are added to the data and the updated df is returned
# modelname: this is used to give the xG row a meaningful name
# regression: is the given regression on which the prediction is based on
# filename: the file for which the prediction should be done, file has to be json
# attributes on which x values the prediction should be based on

def prediction(modelname, regression, df, attributes):
    x = attributes
    xReal = df[attributes]
    xGoal = regression.predict(xReal)
    df[modelname] = xGoal
    return df


def predictionOfSingleValues(values, attributes, regression):
    data = [values]
    predictionDf = pd.DataFrame(data, columns=attributes)
    pred = regression.predict(predictionDf)
    return pred[0]

# method calculates accuracy of the model in comparison to the statsbomb estimation
# the accuracy is defined as the difference between the regression calculation and the statsbomb estimation
# the difference is saved to the data frame
# the dataframe is updated and returned
# the mean of the difference is printed out
def calculateAccuracy(modelname, df):
    nameOfColumn = "difference" + modelname
    df[nameOfColumn] = df[modelname] - df["shot_statsbomb_xg"]
    print("the mean of the difference of ", modelname, " is: ", df[nameOfColumn].mean())
    return df
