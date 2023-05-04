import plotly.express as px
import pandas as pd
from matplotlib.lines import Line2D

from SetUp import JSONtoDF, CONSTANTS
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
import numpy as np
import matplotlib as mpl
from sklearn.cluster import AgglomerativeClustering


# ... read in data
df = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
df = df.loc[(df['y_ball'] >= 16.5) & (df['y_ball'] <= 65)]
df = df.sample(50)
df.reset_index(drop=True, inplace=True)

# Get cluster labels
X = df[['x_coordinate', 'y_coordinate', 'x_ball', 'y_ball']].values
nr_of_clusters = 10
kmeans = KMeans(n_clusters=nr_of_clusters, random_state=0).fit(X)
df['cluster'] = kmeans.labels_

# Get counts per cluster
counts = df['cluster'].value_counts().sort_index()

# Create figure and axis objects
fig, ax = plt.subplots(figsize= (16,12))
img = plt.imread("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Draw/background_pitch/102_120_18_62_penalty.png")
ax.imshow(img, alpha=0.7, extent=[102, 120, 18, 62])

# Plot clusters
for cluster, data in df.groupby('cluster'):
    # Get counts for current cluster
    count = counts[cluster]

    # Plot connection lines
    for i in range(len(data)):
        x1, y1 = data.iloc[i]['x_coordinate'], data.iloc[i]['y_coordinate']
        x2, y2 = data.iloc[i]['x_ball'], data.iloc[i]['y_ball']
        alpha = data.iloc[i]['xP_best_alternative']
        cmap = plt.get_cmap('RdYlGn')
        color = cmap(alpha)
        """
        The thickness of the arrow represents the number of connections in the cluster. 
        The more connections in the cluster, the thicker the arrow.
        """
        ax.arrow(x1, y1, x2-x1, y2-y1, head_width=0.5, head_length=0.5, fc='none', ec=color, lw=count/2, alpha=0.5, length_includes_head=True)

    # Plot end points
    ax.scatter(data['x_ball'], data['y_ball'], s=100, c=data['xP_best_alternative'], cmap='RdYlGn', vmin=0, vmax=1, alpha=0.8, edgecolors='black')

    # Plot start points
    ax.scatter(data['x_coordinate'], data['y_coordinate'], s=10, c='black', alpha=0.8)

# Set axis limits
#ax.set_xlim([min(df['x_coordinate']), max(df['x_ball'])])
#ax.set_ylim([min(df['y_coordinate']), max(df['y_ball'])])

# Set axis labels
ax.invert_yaxis()
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')

# Show plot
# Normalizer
norm = mpl.colors.Normalize(vmin=min(df['xP_best_alternative']), vmax=max(df['xP_best_alternative']))

# creating ScalarMappable
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])

plt.colorbar(sm, ticks=np.linspace(min(df['xP_best_alternative']), max(df['xP_best_alternative']), nr_of_clusters))
plt.show()

