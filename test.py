from SetUp import JSONtoDF, DataManipulation, CONSTANTS
import pandas as pd
import json
import os
import numpy as np
from DecisionEvaluation import evaluationHelper
from SetUp import CONSTANTS, JSONtoDF
import pandas as pd
from Model import  model



dfEM = JSONtoDF.createDF(CONSTANTS.JSONEM2020)
dfWM = JSONtoDF.createDF(CONSTANTS.JSONWM2022)
dfModel = JSONtoDF.createDF("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/JSON/allModelData.json")

