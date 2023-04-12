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

# change xP values of all shots
df_return = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
df_return = evaluate_decision.decisionEvaluation(df_return, "competition")
# reset the index, so a new index is created
df_return.reset_index(drop=True, inplace=True)

df_return.to_json(CONSTANTS.JSONTESTSHOTS)
print("deb")