from SetUp import JSONtoDF,CONSTANTS, DataManipulation
import matplotlib.pyplot as plt
from scipy.stats import shapiro, kstest
import numpy as np
import scipy.stats as stats
import pylab
def check_normal_distribution(df):
    plt.hist(df['angleInRadian'], edgecolor='black', bins=20)
    plt.show()

    shapiro_val, p_val = shapiro(df["angleInRadian"].values.tolist())
    if p_val > 0.05:
        print("data is normal distributed,",shapiro_val, "- pval, ", p_val)
        return True
    else:
        print("data is not normal distributed,", shapiro_val, "- pval, ", p_val)
        return False

df = JSONtoDF.createDF(CONSTANTS.JSONTRAINSHOTS)
logAngleList = []
for shot in range(len(df)):
    # if the shot is equal to 0, then the penalty has to be limited
    # the reason for that is that log(0) is undefined,
    # we therefore limit the penalty to maximal -5 --> log(0.00001)
    if df['angleInRadian'][shot] < 0.000001:
        logAngleList.append(np.log10(0.001))
    else:
        # else create a penalty
        #if df['match_id'][shot] == 266254 and df['minute'][shot] == 74:
        w = shot
        x = df['angleInRadian'][shot]
        y = np.log(df['angleInRadian'][shot])
        z = -np.log(df['angleInRadian'][shot])
        #(-) weil kleine Winkel führen zu negativen penalties, der penalty soll aber je höher, desto schlimmer sein
        logAngleList.append(np.log10(df['angleInRadian'][shot]))
df['log10_angle'] = logAngleList

df.to_csv("C:/Users/lenna/Downloads/dfTest.csv")
#stats.probplot(df['log_angle'], dist="norm", plot=pylab)
#pylab.show()

#check_normal_distribution(df)