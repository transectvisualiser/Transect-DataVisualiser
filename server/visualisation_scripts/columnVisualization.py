import matplotlib.pyplot as plt
import pandas as pd


file_path = "General List (CSES-NS-Summary-Evaluations).csv"
df = pd.read_csv(file_path)

# Extract relevant columns
df_filtered = df[['Beach', 'Region', 'Type of sediment']].dropna()
# Count distinct beaches per sediment type and region
sediment_counts = df_filtered.groupby(['Type of sediment', 'Region'])['Beach'].nunique().unstack(fill_value=0)

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
sediment_counts.plot(kind='bar', stacked=False, ax=ax, colormap='plasma')


# Labels and title
ax.set_xlabel("Type of Sediment")
ax.set_ylabel("Number of Distinct Beaches")
ax.set_title("Beaches by Sediment Type and Region")
ax.legend(title="Region", bbox_to_anchor=(1.05, 1), loc='upper left')

# Show plot
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


