from SetUp.Get_Training_Data import get_training_df
from SetUp import testing, JSONtoDF, CONSTANTS
from Model import create_model, model_info

dfTrain = JSONtoDF.createDF(CONSTANTS.JSONTRAINSHOTS)
#create the model
model = create_model.create_model_glm(df=dfTrain, attributes=CONSTANTS.ATTRIBUTES)
model_info.show_info(model)
print("i created the model")
#get df
df = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
print("i created the test data")

df.reset_index(drop=True, inplace=True)
dfTest = testing.MANIPULATEdf(df, CONSTANTS.JSONTESTSHOTS)
print("i manipulated the test data")
print("I AM DONE DONE")