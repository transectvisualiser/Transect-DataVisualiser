import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage


file_path = "General List (CSES-NS-Summary-Evaluations).csv"
data = pd.read_csv(file_path)


env_features = ['Dunes']
X = data[env_features]


region_means = data.groupby('Region')[env_features].mean()

Z = linkage(region_means, method='ward', metric='euclidean')

plt.figure(figsize=(12, 7))
dendrogram(
    Z,
    labels=region_means.index,
    leaf_rotation=45,
    leaf_font_size=12,
)


plt.title('Dendrogram of Regions based on the average of Dunes.', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Regions', fontsize=12, labelpad=10)
plt.ylabel('Distance (Ward\'s method)', fontsize=12, labelpad=10)

plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()


plt.show()

