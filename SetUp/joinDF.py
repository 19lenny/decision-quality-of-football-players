import pandas as pd
from SetUp import CONSTANTS


def concat(dataframes_as_list):
    df_all = pd.DataFrame()
    for df in dataframes_as_list:
        df_all = pd.concat([df_all, df])
    return df_all
