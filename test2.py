import math
import os
import json
import pandas as pd
from SetUp import CONSTANTS, DataManipulation, JSONtoDF
from scipy.stats import expon
from decimal import *
import numpy as np
from scipy.stats import pearsonr
from Model import model_info
from SetUp.DecisionEvaluation import evaluationHelper, evaluate_decision

df_train = JSONtoDF.createDF(CONSTANTS.JSONTRAINSHOTS)

df_test = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
coeff = pearsonr(df_test["shot_statsbomb_xg"], df_test["xG"])
print(coeff)

