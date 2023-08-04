from SetUp import CONSTANTS, JSONtoDF
from scipy.stats import gaussian_kde
import numpy as np
import matplotlib.pyplot as plt

df_return_test = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
biins = 30

# Remove invalid values
xg_values = df_return_test['xG'].dropna().replace([np.inf, -np.inf], np.nan)
xg_values_statsbomb = df_return_test['shot_statsbomb_xg'].dropna().replace([np.inf, -np.inf], np.nan)

# Create the histogram plot for xg_values
plt.hist(xg_values, bins=biins, density=True, edgecolor='black', alpha=0.5, label="xG Distribution from xG Model")

# Calculate the kernel density estimate (KDE) for xg_values
x = np.linspace(xg_values.min(), xg_values.max(), 100)
kde = gaussian_kde(xg_values, bw_method=None)  # Automatic bandwidth estimation
y = kde(x)

# Scale the KDE line to match the histogram peak
scale_factor = np.max(np.histogram(xg_values, bins=biins, density=True)[0]) / np.max(y)
y *= scale_factor

# Add the KDE line to the plot
plt.plot(x, y, color='blue')

# Create the histogram plot for xg_values_statsbomb
plt.hist(xg_values_statsbomb, bins=biins, density=True, edgecolor='black', alpha=0.5, label="xG Distribution from StatsBomb xG values")

# Calculate the kernel density estimate (KDE) for xg_values_statsbomb
kde_statsbomb = gaussian_kde(xg_values_statsbomb, bw_method=None)  # Automatic bandwidth estimation
y_statsbomb = kde_statsbomb(x)

# Scale the KDE line to match the histogram peak
scale_factor_statsbomb = np.max(np.histogram(xg_values_statsbomb, bins=biins, density=True)[0]) / np.max(y_statsbomb)
y_statsbomb *= scale_factor_statsbomb


plt.plot(x, y_statsbomb, color='orange')


plt.title('Comparison of xG Distribution')
plt.xlabel('xG')
plt.ylabel('Density')

plt.legend()


plt.show()
