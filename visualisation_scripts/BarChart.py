import pandas as pd
import matplotlib.pyplot as plt

# This is the local file path for my CSV file for the Bar Chart
file_path = "General List (CSES-NS-Summary-Evaluations).csv"

# This is to load the dataframe
df = pd.read_csv(file_path)

# Group by region and the beach width as per the data that I have and getting the mean of each region.
beach_width_by_region = df.groupby("Region")["Beach width"].mean()

# This is where the Bar chart is being ploted.
plt.figure(figsize=(20, 6))
beach_width_by_region.plot(kind="bar", color="blue")

# Formatting the th bar chart, Creating titles and formating the rotation for the chart.
plt.xlabel("Region")
plt.ylabel("Average Beach Width")
plt.title("Average Beach Width by Region")
plt.xticks(rotation=0)

# To show the Bar Chart.
plt.show()
