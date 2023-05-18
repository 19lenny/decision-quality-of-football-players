import math

import CONSTANTS, JSONtoDF
from Model import create_model, model_info

from SetUp.DecisionEvaluation import evaluate_decision
import numpy as np



df_return = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)

df_return.to_csv("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/SPSS/dfTest/dfTest.csv")

df_return = JSONtoDF.createDF(CONSTANTS.JSONTRAINSHOTS)
df_return.to_csv("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/SPSS/dfTrain/dfTrain.csv")


 


