import math
import os
import json
import pandas as pd
from SetUp import CONSTANTS, DataManipulation, JSONtoDF
from scipy.stats import expon
from decimal import *
import numpy as np
from scipy.stats import pearsonr
from statsbombpy import sb
from Model import model_info
from SetUp.DecisionEvaluation import evaluationHelper, evaluate_decision

df_train = JSONtoDF.createDF(CONSTANTS.JSONTRAINSHOTS)

df_test = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
coeff = pearsonr(df_test["shot_statsbomb_xg"], df_test["xG"])
print(coeff)

get_all_events_of_this_match = sb.events(7541)
get_all_events_of_this_match = get_all_events_of_this_match[["minute", "period", "team", "player", "type", "shot_body_part", "play_pattern", "shot_type", "shot_statsbomb_xg"]]

