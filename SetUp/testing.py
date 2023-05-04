from statsbombpy import sb
import pandas as pd
from SetUp import DataManipulation, CONSTANTS, JSONtoDF
from Model import model_info
from SetUp.DecisionEvaluation import evaluate_decision
from SetUp import TM_values

def MANIPULATEdf(df_return, save_path):

    """
        df_return = DataManipulation.addDeltaGKToOptimalLine(df_return)
        df_return.to_json(save_path)
        # add xGoal, calculated by me
        df_return = model_info.prediction(df_return)
        df_return.to_json(save_path)
    """
    df_return = evaluate_decision.decisionEvaluation(df_return, "competition")

    df_return.reset_index(drop=True, inplace=True)

    df_return.to_json(save_path)

    print("i am finished with competition: ", "testing --> get testing dataframe")
    return df_return


