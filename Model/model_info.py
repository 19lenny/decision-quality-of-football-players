

from SetUp import JSONtoDF
import pandas as pd
from SetUp import CONSTANTS




# this method prints the information about a given regression
def show_info(regression):
    print(regression.summary())


# this method predicts the xG with the help of a given model
# the prediction explicitely predicts xG and NOT xMisses
# the predictions are added to the data and the updated df is returned
# modelname: this is used to give the xG row a meaningful name
# regression: is the given regression on which the prediction is based on
# filename: the file for which the prediction should be done, file has to be json
# attributes on which x values the prediction should be based on

def prediction(df):
    xReal = df[CONSTANTS.ATTRIBUTES]
    xGoal = CONSTANTS.REGRESSION_MODEL.predict(xReal)
    df[CONSTANTS.MODELNAME] = xGoal
    return df


def predictionOfSingleValues(values, attributes):
    """
    formular of prediction is: exp(regression*values)/(1+exp(regression*values))
    source: https://stats.stackexchange.com/questions/441561/get-equation-from-glm-coefficients-calculate-y-manually
    """
    data = [values]
    predictionDf = pd.DataFrame(data, columns=attributes)
    pred = CONSTANTS.REGRESSION_MODEL.predict(predictionDf)
    return pred[0]

# method calculates accuracy of the model in comparison to the statsbomb estimation
# the accuracy is defined as the difference between the regression calculation and the statsbomb estimation
# the difference is saved to the data frame
# the dataframe is updated and returned
# the mean of the difference is printed out
def calculateAccuracy(df, championship):
    nameOfColumn = "difference" + CONSTANTS.MODELNAME
    df[nameOfColumn] = df[CONSTANTS.MODELNAME] - df["shot_statsbomb_xg"]
    print("the mean of the difference of ", CONSTANTS.MODELNAME,"at", championship,"is: ", df[nameOfColumn].mean())
    return df


