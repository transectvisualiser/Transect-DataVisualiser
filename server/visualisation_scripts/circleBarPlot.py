import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Read the CSV file.
df = pd.read_csv('General List (CSES-NS-Summary-Evaluations).csv')
df['Dunes'] = df['Dunes'].astype(float)

unique_dunes = np.sort(df['Dunes'].unique())

# Generate distinct colors for each unique dune value using the "plasma" colormap.
cmap = plt.cm.get_cmap("plasma", len(unique_dunes))
group_colors = {d: cmap(i) for i, d in enumerate(unique_dunes)}

df_sorted = df.sort_values('Dunes')

beaches = df_sorted['Beach']
dunes = df_sorted['Dunes']

N = len(beaches)

# Compute the angle for each bar.
angles = np.linspace(0, 2 * np.pi, N, endpoint=False)

inner_radius = 1.5

# Normalize the dune values to determine bar heights.
max_dunes = dunes.max()
min_dunes = dunes.min()
bar_heights = (dunes - min_dunes) / (max_dunes - min_dunes) * 2
bar_heights = bar_heights.apply(lambda x: 0.1 if x == 0 else x)

# Widen the bars by increasing the angular width.
base_width = 2 * np.pi / N
bar_width = base_width * 1

fig, ax = plt.subplots(figsize=(11, 11), subplot_kw={'projection': 'polar'})

# Plot each bar
for angle, height, label, dune_val in zip(angles, bar_heights, beaches, df_sorted['Dunes']):
    ax.bar(angle, height, width=bar_width, bottom=inner_radius,
           color=group_colors[dune_val], edgecolor='black')

# Add labels for each bar.
for angle, height, label in zip(angles, bar_heights, beaches):
    rotation = np.degrees(angle)
    alignment = "left"
    if 90 < np.degrees(angle) < 270:
        rotation += 180
        alignment = "right"
    ax.text(angle, inner_radius + height + 0.05, label, rotation=rotation,
            rotation_mode='anchor', horizontalalignment=alignment,
            verticalalignment='center', fontsize=8)

ax.set_axis_off()

# legend mapping each unique dune value to its color.
legend_elements = [Patch(facecolor=group_colors[d], edgecolor='black', label=str(d)) for d in unique_dunes]
plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.1, 1.1))

plt.title("Circular Bar Plot of Dunes by Beach", va='bottom')
# plt.savefig("circlePlot.png", dpi=500, bbox_inches='tight')

plt.show()


