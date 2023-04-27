
import pandas as pd
import numpy as np


df_test = pd.read_json("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/" 
                    "Masterarbeit/Thesis/thesis/JSON/Train_Set_Shots.json")

print("deb")

def log_angle(df):
    logAngleList = []
    for shot in range(len(df)):
        # if the shot is equal to 0, then the penalty has to be limited
        # the reason for that is that log(0) is undefined,
        # we therefore limit the penalty to maximal -5 --> log(0.00001)
        if df['angleInRadian'][shot] < 0.000001:
            logAngleList.append(np.log(0.001))
        else:
            # else create a penalty
            #if df['match_id'][shot] == 266254 and df['minute'][shot] == 74:
            w = shot
            x = df['angleInRadian'][shot]
            y = np.log(df['angleInRadian'][shot])
            z = -np.log(df['angleInRadian'][shot])
            #(-) weil kleine Winkel führen zu negativen penalties, der penalty soll aber je höher desto schlimmer sein
            logAngleList.append(np.log(df['angleInRadian'][shot]))
    df['log_angle'] = logAngleList
    return df

df_test = log_angle(df_test)

df_test.to_json("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/" 
                    "Masterarbeit/Thesis/thesis/JSON/Train_Set_Shots.json")

