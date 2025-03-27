import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

file_paths = {
    "beach_profile": os.path.join("..", "data", "beach-profile.json"),
    "cocorahs": os.path.join("..", "data", "cocorahs.json"),
    "weather_everyday": os.path.join("..", "data", "weather-everyday.json")
}

for key, path in file_paths.items():
    print(f"Checking file: {path}")
    if not os.path.exists(path):
        print(f"Error: {path} not found")
        exit()
    else:
        print(f"Found: {path}")

with open(file_paths["beach_profile"], 'r') as file:
    beach_data = json.load(file)
beach_df = pd.DataFrame(beach_data["results"])

with open(file_paths["cocorahs"], 'r') as file:
    cocorahs_data = json.load(file)
cocorahs_df = pd.DataFrame(cocorahs_data["results"])

with open(file_paths["weather_everyday"], 'r') as file:
    weather_data = json.load(file)
weather_daily_df = pd.DataFrame(weather_data["observations"])

print("Beach Profile Data:", beach_df.shape)
print("CoCoRaHS Data:", cocorahs_df.shape)
print("Daily Weather Data:", weather_daily_df.shape)

elevation_cols = [col for col in beach_df.columns if "Point_" in col]
beach_elevations = beach_df[elevation_cols].astype(float)

plt.figure(figsize=(10, 6))
sns.boxplot(data=beach_elevations, orient="h", color="skyblue")
plt.title("Beach Profile Elevation Distribution")
plt.xlabel("Elevation (m)")
plt.yticks(np.arange(0, len(elevation_cols), step=5))  # Reduce y-axis labels for clarity
plt.grid()
plt.show(block=False)
plt.pause(2)

precip_by_station = cocorahs_df.groupby("stationName")["precip"].sum()
precip_by_station = precip_by_station[precip_by_station > 0]  # Remove stations with zero precipitation

plt.figure(figsize=(10, 5))
plt.scatter(precip_by_station.index, precip_by_station.values, color='green', s=200)
plt.title("Total Precipitation Recorded at Different Stations")
plt.xlabel("Station")
plt.ylabel("Precipitation (inches)")
plt.xticks(rotation=45)
plt.grid(axis='y')

for i, txt in enumerate(precip_by_station.values):
    plt.annotate(f'{txt:.2f}', (precip_by_station.index[i], precip_by_station.values[i]), 
                 ha='center', va='bottom', fontsize=12, color='black', xytext=(0, 5), textcoords="offset points")

plt.show(block=False)
plt.pause(2)

weather_daily_df["tempAvg"] = weather_daily_df["metric"].apply(lambda x: x["tempAvg"])

plt.figure(figsize=(8, 6))
sns.violinplot(y=weather_daily_df["tempAvg"], color="lightblue")
plt.title("Daily Temperature Distribution (Violin Plot)")
plt.ylabel("Temperature (°C)")
plt.grid()
plt.show()
