# sources
# https://towardsdatascience.com/building-a-logistic-regression-in-python-step-by-step-becd4d56c9c8
# https://www.youtube.com/watch?v=wHOgINJ5g54
import statsmodels.api as sm
import statsmodels.formula.api as smf

# create a logistic regression with an intercept
# filename is the filelocation for which a model should be created, the file has to be in json format
# attributes are the attributes that the model should learn on (x_values)
"""
GLM is a generalized linear model and Logit Model is specific to models with binary classification. 
While using GLM model you have to mention the parameter family which can be binomial (logit model), Poisson etc. 
This parameter is not required in Logit model as its only for binary output. 
source: https://stackoverflow.com/questions/62622779/what-is-the-difference-between-glm-and-logit-model-with-statsmodels#:~:text=GLM%20is%20a%20generalized%20linear,its%20only%20for%20binary%20output.
the output is the same as with 
log_reg = smf.logit("goal ~ angleInRadian + distance_to_goal_centre", data = df).fit()
i tested it"""
"""
having the data with no intercept is a stupid idea:
It is almost always necessary. I say almost always because it changes the interpretation of the other coefficients. Leaving out the column of 1s may be fine when you are regressing the outcome on categorical predictors, but often we include continuous predictors.

Let's compare a logistic regression with and without the intercept when we have a continuous predictor. Assume the data have been mean centered. Without the column of 1s, the model looks like

logit(p(x)1−p(x))=βx

When x=0
 (i.e. when the covariate is equal to the sample mean), then the log odds of the outcome is 0, which corresponds to p(x)=0.5
. So what this says is that when x
 is at the sample mean, then the probability of a success is 50% (which seems a bit restrictive).

If we do have the intercept, the model is then

logit(p(x)1−p(x))=β0+βx

Now, when x=0
 the log odds is equal to β0
 which we can freely estimate from the data.

In short, unless you have good reason to do so, include the column of 1s.

source: https://stats.stackexchange.com/questions/440242/statsmodels-logistic-regression-adding-intercept
"""
def create_model_glm(df, attributes):

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
    model = smf.glm(formula="goal ~ " + model, data=df,
                         family=sm.families.Binomial()).fit()
    # return the model
    return model