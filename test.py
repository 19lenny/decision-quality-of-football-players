import json

import numpy as np
from statsbombpy import sb
import pandas as pd
from SetUp import DataManipulation, CONSTANTS, JSONtoDF
from Model import model_info
from SetUp.DecisionEvaluation import evaluate_decision
from SetUp import TM_values
from Hypothesis_Competition_Stage import DataManipulation_competition_stage


df_test = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
df_test = df_test.loc[(df_test['match_id'] == 3857269) & (df_test['minute'] == 26)].head(1)
df_test.reset_index(drop=True, inplace=True)
freeze = df_test['shot_freeze_frame'][0]

# the event comes in a json like format
# transform it to a real json
freeze_frame = json.dumps(freeze)
# save the json (name = sample.json), so we can import it to a dataframe
with open("test.json", "w") as outfile:
    outfile.write(freeze_frame)