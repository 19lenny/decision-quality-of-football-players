import math
import os
import json
import pandas as pd
from SetUp import CONSTANTS, DataManipulation, JSONtoDF
from scipy.stats import expon
from decimal import *
import numpy as np
from Model import model_info
from SetUp.DecisionEvaluation import evaluationHelper, evaluate_decision

df_return = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
df_description = df_return.describe()
df_description.to_excel("old_decription.xlsx")