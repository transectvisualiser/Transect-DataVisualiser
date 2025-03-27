import json
import squarify
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

# Load the JSON file containing the weather observations
with open('../data/weather-everyday.json', 'r') as file:
    data = json.load(file)

# Extract the observations from the JSON
observations = data.get('observations', [])

# Extract the average temperature from each observation's metric field
temps = [obs['metric']['tempAvg'] for obs in observations
         if 'metric' in obs and 'tempAvg' in obs['metric']]

# Count the frequency of each average temperature value
temp_counts = Counter(temps)

# sizes: number of observations for each temperature
# labels: a text label for each block (showing temperature and count)
sizes = list(temp_counts.values())
labels = [f"Temp: {temp}°C\nCount: {count}" for temp, count in temp_counts.items()]

num_categories = len(temp_counts)
colors = plt.cm.viridis(np.linspace(0, 1, num_categories))

# Create the treemap plot using squarify
plt.figure(figsize=(12, 8))
squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.8, pad=True)

plt.title("Distribution of Average Temperatures from Weather Observations", fontsize=18)
plt.axis('off')

plt.show()
