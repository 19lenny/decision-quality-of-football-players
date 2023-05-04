from SetUp.Get_Training_Data import get_training_df
from SetUp import testing, JSONtoDF, CONSTANTS
from Model import create_model, model_info

df_all = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
#group 1 is the expensive group, group 0 is cheap group
df_all['group_market_value'] = np.where(df_all['value'] >= df_all['value'].median(), 1, 0)
df_all.to_csv("C:/Users/lenna/Downloads/df_spss.csv")