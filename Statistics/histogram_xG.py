from SetUp import CONSTANTS, JSONtoDF
from scipy.stats import gaussian_kde
import numpy as np
import matplotlib.pyplot as plt

df_return_test = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)

# Remove invalid values (NaN and inf)
xg_values = df_return_test['xG'].dropna().replace([np.inf, -np.inf], np.nan)

# Create the histogram plot
plt.hist(xg_values, bins=30, density=True, edgecolor='black', alpha=0.5)

# Calculate the kernel density estimate (KDE)
x = np.linspace(xg_values.min(), xg_values.max(), 100)
kde = gaussian_kde(xg_values, bw_method=None)  # Automatic bandwidth estimation
y = kde(x)

# Scale the KDE line to match the histogram peak
scale_factor = np.max(np.histogram(xg_values, bins=30, density=True)[0]) / np.max(y)
y *= scale_factor

# Add the KDE line to the plot
plt.plot(x, y, color='red')

# Customize the plot
plt.title('Histogram of xG with KDE')
plt.xlabel('xG')
plt.ylabel('Density')

# Display the plot
plt.show()
