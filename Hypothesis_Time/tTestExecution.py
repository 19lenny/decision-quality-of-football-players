from typing import List

import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from SetUp import JSONtoDF, CONSTANTS
def tTestTime(df, start_period, end_period):
    """
    This method sorts and groups a given dataframe. The sorted dataframe evaluates if the decision of player changes over played minutes with help of a tTest.
    :param df: the dataframe, for which the tTest should be done for
    :param start_period: from which period the tTest should be done for, e.g. first half = 1
    :param end_period: until which period should the work be done, e.g. second half = 2
    :return: is the result of the tTest
    """
    # empty lists to add to the tTest as helping variables
    minute = []
    period = []
    # only take the shots that are done within the given boundaries
    df = df.loc[(df['period'] >= start_period) & (df['period'] <= end_period)]
    # group by period and minute, so it is already sorted. and calculated the mean of every minute in every period
    # reset index so a for loop can be done over the dataframe
    df = df.groupby(['period','minute'])["xG_Delta_decision_alternative"].mean().reset_index()
    #list to save the results
    t_stat: List[float] = [0.0] * len(df)
    p_values: List[float] = [0.0] * len(df)

    #go through all means of the grouped dataframe
    for index in range(len(df)):
        #save minute and period
        minute.append(df['minute'][index])
        period.append(df['period'][index])
        #take all shots until this minute (=index | period)
        shotValuesOne = df['xG_Delta_decision_alternative'].iloc[:index].values.tolist()
        # take all other shots (point index is in this dataframe)
        shotValuesTwo = df['xG_Delta_decision_alternative'].iloc[index:].values.tolist()
        # tTest only works if at least two entries are given, therefore the calculations should only be done for at least 2 mean values
        if len(shotValuesOne) <= 1 or (len(shotValuesTwo) <= 1):
            t_stat[index], p_values[index] = 0, 0
        else:
            # calculate the t-test statistics for the current minute
            t_stat[index], p_values[index] = ttest_ind(shotValuesOne, shotValuesTwo)

    # add all the calculations to a dataframe and return it

    dataTime = {'minute': minute,
                'T-stat': t_stat,
                'P-Val': p_values,
                'period': period
                }
    dfTime = pd.DataFrame(dataTime)
    return dfTime

def tTestRegularvsOT(df, end_period_regular, start_period_OT):
    """
      This method evaluates if the decision of players changes if they play over time or not
      :param df: the dataframe, which the evaluation should be done for
      :param start_period_OT: when does the overtime start
      :param end_period_regular: when is the regular time over
      :return: is the result of the tTest
      """
    #todo: normally only shots are taken into account that played OT, here all shots are taken into account that also played regular
    # thats wrong

    # only take the shots that are done within the given boundaries
    dfReg = df.loc[(df['period'] <= end_period_regular)]
    dfOT = df.loc[(df['period'] >= start_period_OT)]

    #all values
    valuesReg = dfReg["xG_Delta_decision_alternative"].values.tolist()
    dfOT = dfOT["xG_Delta_decision_alternative"].values.tolist()

    t_stat, p_value = ttest_ind(valuesReg, dfOT)
    dataTime = {'T-stat': [t_stat],
                'P-Val': [p_value]
                }
    dfTime = pd.DataFrame(dataTime)
    return dfTime

