import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('visualisation_scripts/General List (CSES-NS-Summary-Evaluations).csv')

columns = ['Region', 'Cliff height', 'Noise disturbance', 'Vegetation cover']
df = pd.DataFrame(data, columns=columns)

df = pd.DataFrame(data, columns=columns)
grouped_df = df.groupby('Region').agg({
    'Cliff height': 'mean',
    'Noise disturbance': 'mean',
    'Vegetation cover': 'mean'
}).round(2)  

grouped_df = grouped_df.reset_index()

fig, ax = plt.subplots(figsize=(8, 4))

ax.axis('off')
ax.axis('tight')

table = ax.table(cellText=grouped_df.values, colLabels=grouped_df.columns, cellLoc='center', loc='center', colLoc='center', cellColours=[['#f1f1f2']*len(columns)]*len(grouped_df), colColours=['#f1f1f2']*len(columns), colWidths=[0.2]*len(columns))

table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1.2, 1.5)

plt.show()