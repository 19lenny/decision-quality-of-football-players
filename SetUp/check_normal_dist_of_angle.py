from SetUp import JSONtoDF,CONSTANTS, DataManipulation
import matplotlib.pyplot as plt
from scipy.stats import shapiro, kstest
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
df.to_csv("C:/Users/lenna/Downloads/dfTest.csv")
#stats.probplot(df['log_angle'], dist="norm", plot=pylab)
#pylab.show()

#check_normal_distribution(df)