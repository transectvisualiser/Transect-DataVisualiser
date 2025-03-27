import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

# File path
file_path = "General List (CSES-NS-Summary-Evaluations).csv"

# Read the CSV file
df = pd.read_csv(file_path)

# Extract relevant columns and drop missing values
df_filtered = df[['Beach', 'Litter']].dropna()  #dropna Clears Nulls

# Litter Data 
litter_data = df_filtered["Litter"].tolist()

# Ploting on Graph bins depending on unique levels in data
expected_levels = {1, 2, 3, 4, 5}
unique_levels = set(litter_data)
missing_count = len(expected_levels - unique_levels)

if missing_count == 0:
    bins = 5
elif missing_count == 1:
    bins = 4
elif missing_count == 2:
    bins = 3
elif missing_count == 3:
    bins = 2
else:
    bins = 1  # If only one category remains, one bin

plt.hist(litter_data, bins=bins, edgecolor='black', alpha=0.7)
plt.xticks([1, 2, 3, 4, 5])


#Labeling Axis
plt.xlabel("Litter Level")  # Label for X-axis
plt.ylabel("Number Of Beaches")  # Label for Y-axis
plt.title("Litter Distribution Level Across Beaches") # Labels the Title 

#Displays the Graph
plt.show()








