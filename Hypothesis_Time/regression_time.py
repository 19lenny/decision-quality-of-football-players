from SetUp import JSONtoDF, CONSTANTS
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

df = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
#only take first and second half and not third and fourth period
df = df.loc[(df["period"] == 1) | (df["period"] == 2)]
#https://medium.com/analytics-vidhya/implementing-linear-regression-using-sklearn-76264a3c073c
#what is a dummy variabel
X = df[['period']]
X['is_first_half'] = np.where(X['period'] == 1, 1, 0)
X = X['is_first_half']
Y = df['xG_Delta_decision_alternative']
print(X.head())


X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.4, random_state=101)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)
model = LinearRegression()
model.fit(X_train,y_train)
# print the intercept
print(model.intercept_)
coeff_parameter = pd.DataFrame(model.coef_,X.columns,columns=['Coefficient'])
print(coeff_parameter)

# das gseht scheisse us gregi