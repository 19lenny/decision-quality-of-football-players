from statsbombpy import sb
import pandas as pd
from SetUp import DataManipulation, CONSTANTS, JSONtoDF
from Model import model_info
from SetUp.DecisionEvaluation import evaluate_decision
from SetUp import TM_values



TRAIN = JSONtoDF.createDF(CONSTANTS.JSONTRAINSHOTS)
TEST = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)

