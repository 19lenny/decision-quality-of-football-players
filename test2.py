
import pandas as pd
from SetUp import DataManipulation
import numpy as np


df_train = pd.read_json("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/" 
                    "Masterarbeit/Thesis/thesis/JSON/Train_Set_Shots.json")





df_train = DataManipulation.log_penalty(df_train)

df_train.to_json("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/" 
                    "Masterarbeit/Thesis/thesis/JSON/Train_Set_Shots.json")

