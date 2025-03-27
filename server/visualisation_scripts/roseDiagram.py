import json
import numpy as np
import matplotlib.pyplot as plt

with open("../data/weather-everyday.json", "r") as f:
    data = json.load(f)

# Extract wind direction values (winddirAvg) from each observation
wind_dirs = [obs["winddirAvg"] for obs in data["observations"] if "winddirAvg" in obs]

# Define bins (e.g., every 30 degrees for a total of 12 bins)
num_bins = 12
bins = np.linspace(0, 360, num_bins + 1)  # 13 edges for 12 bins

# Bin the wind direction data
counts, _ = np.histogram(wind_dirs, bins=bins)

# Compute the center angle for each bin in radians
bin_width = (bins[1] - bins[0])
angles = np.deg2rad(bins[:-1] + bin_width/2)

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, polar=True)
bars = ax.bar(angles, counts, width=np.deg2rad(bin_width), bottom=0.0, align='center', edgecolor='k', color='cyan')

ax.set_theta_zero_location('N')  # Set North (0°) at the top
ax.set_theta_direction(-1)      # Set the direction clockwise
ax.set_title("Wind Rose Diagram", va='bottom')

plt.show()
