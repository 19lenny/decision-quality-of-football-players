from typing import List
from scipy.stats import ttest_ind
import pandas as pd
import scipy.stats as stats
from SetUp import JSONtoDF, CONSTANTS, DataManipulation
from scipy.stats import levene
import numpy as np

df_train = JSONtoDF.createDF(CONSTANTS.JSONTRAINSHOTS)
df_train.to_csv("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/SPSS/dfTrain/dfTrain.csv")

df_test = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
df_test.to_csv("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/SPSS/dfTest/dfTest.csv")
