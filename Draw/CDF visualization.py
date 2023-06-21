import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon


# Generate the range of values for the x-axis
possible_range_of_sec = np.arange(0, 1.3, 0.001)  # Adjust the range and number of points as needed

# Calculate the CDF values
possible_xP_values = expon.cdf(possible_range_of_sec, 0, 1 / 4.30)

# Plotting the CDF
plt.plot(possible_range_of_sec, possible_xP_values, label='CDF, Lambda=4.30/second')
plt.plot([1, 1], [0, 1], 'r--', label='CDF at 1 sec')
plt.plot([0, 1], [0.985, 0.985], 'r--')
plt.xlabel('Delta Time between Teamplayer and Opponent')
plt.ylabel('Cumulative Probability')
plt.title('Exponential Cumulative Distribution Function')
plt.grid(True)
plt.legend()
plt.show()
