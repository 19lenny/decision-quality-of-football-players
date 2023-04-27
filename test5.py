from matplotlib import rcParams, pyplot as plt
from scipy.stats import shapiro

from Model import create_model, model_info
from SetUp import JSONtoDF, DataManipulation, CONSTANTS
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# summary of training data
attributes = ['distance_to_goal_centre', 'log_angle']
df = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
#df = DataManipulation.log_angle(df)



# Create a histogram
plt.hist(df['log_angle'], bins=40)  # Specify number of bins as needed
# Set x-axis label
plt.xlabel('LOG(angle)')
# Set y-axis label
plt.ylabel('Frequency')
# Set plot title
plt.title('Residual Histogram log(angle radian)')
# Show the plot
plt.show()

# Create a histogram
plt.hist(df['distance_to_goal_centre'], bins=40)  # Specify number of bins as needed
# Set x-axis label
plt.xlabel('angle')
# Set y-axis label
plt.ylabel('Frequency')
# Set plot title
plt.title('Residual Histogram angle radian')
# Show the plot
plt.show()




shap_a, p_val_a = shapiro(df['distance_to_goal_centre'])
shap_log, p_val_log = shapiro(df['log_angle'])


"""
Die Teststatistik W beim Shapiro-Wilk-Test ist ein Maß dafür, wie gut die Daten mit der Normalverteilung übereinstimmen.
Ein höherer Wert von W deutet auf eine bessere Übereinstimmung mit der Normalverteilung hin, 
während ein niedrigerer Wert von W auf eine schlechtere Übereinstimmung oder eine potenzielle Abweichung von der Normalverteilung hindeutet.
Die Interpretation der Teststatistik W allein ist jedoch nicht ausreichend, 
um ein endgültiges Urteil über die Normalverteilung der Daten zu fällen. 
Stattdessen sollte die Teststatistik W im Zusammenhang mit dem kritischen Wert oder dem p-Wert des Tests betrachtet werden, 
basierend auf dem festgelegten Signifikanzniveau (auch als alpha-Niveau bezeichnet).
"""