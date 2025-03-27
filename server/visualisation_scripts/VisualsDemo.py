import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# --- Configuration ---
CSV_FILENAME = "General List (CSES-NS-Summary-Evaluations).csv"
FILE_PATH = "C:/Users/Praan/Desktop/CSCI 3691/General List (CSES-NS-Summary-Evaluations).csv"

# --- Data Loading and Preprocessing ---
try:
    df = pd.read_csv(FILE_PATH)
    print(f"Data successfully loaded from: {FILE_PATH}")
except FileNotFoundError:
    print(f"Error: File not found at: {FILE_PATH}")
    exit()
except Exception as e:
    print(f"Error reading CSV: {e}")
    exit()

# --- Descriptive Statistics ---
print("\nDescriptive Statistics:")
print(df.describe())

# --- Unique Visualizations ---
def generate_unique_visualizations(df):

    # --- 1.  Distribution of 'Beach width' grouped by 'CSES Label' (Seaborn) ---
    plt.figure(figsize=(10, 6))
    sns.violinplot(x='CSES Label', y='Beach width', data=df, palette='viridis')
    plt.title("Distribution of Beach Width by CSES Label")
    plt.xlabel("CSES Label")
    plt.ylabel("Beach Width")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


    # --- 2. Scatter Plot of Latitude vs. Longitude colored by Access Type (Matplotlib)---
    plt.figure(figsize=(8, 6))
    for access_type in df['Access type'].unique():
        subset = df[df['Access type'] == access_type]
        plt.scatter(subset['Longitude'], subset['Latitude'], label=access_type)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Beach Locations Colored by Access Type')
    plt.legend()
    plt.show()


    # --- 3. Bar Chart of Average Cliff Height by Region (Matplotlib) ---
    avg_cliff_height = df.groupby('Region')['Cliff height'].mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    avg_cliff_height.plot(kind='bar', color='skyblue')
    plt.title("Average Cliff Height by Region")
    plt.xlabel("Region")
    plt.ylabel("Average Cliff Height")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


    # --- 4. Count Plot of 'Type' of Beach (Seaborn) ---
    plt.figure(figsize=(8, 6))
    sns.countplot(x='Type', data=df, palette='muted')
    plt.title("Count of Beaches by Type")
    plt.xlabel("Type of Beach")
    plt.ylabel("Count")
    plt.show()

    # --- 5.  Box Plot of "D Value" by "Beach colour" (Seaborn) ---
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="Beach colour", y="D Value", data=df, palette="pastel")
    plt.title("Box Plot of D Value by Beach Colour")
    plt.xlabel("Beach Colour")
    plt.ylabel("D Value")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    # --- 6.  Scatter Plot Matrix (Pair Plot) for Numerical Features (Seaborn) ---
    numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
    if len(numerical_cols) > 1:
        plt.figure(figsize=(12, 12))
        sns.pairplot(df[numerical_cols[:5]])  # Limit to first 5 for readability
        plt.suptitle("Pair Plot of Numerical Features (First 5)", y=1.02)
        plt.show()
    else:
        print("Not enough numerical columns for pair plot.")


    # --- 7. Interactive Map of Beaches Colored by CSES Label (Plotly) ---
    fig = px.scatter_geo(df,
                         lat="Latitude",
                         lon="Longitude",
                         color="CSES Label",
                         hover_data=["Beach", "Region"],
                         title="Map of Beaches Colored by CSES Label",
                         scope="north america") # or specify a bounding box
    fig.update_layout(
        geo = dict(
            center=dict(lat=45, lon=-63),  # Approximate center of Nova Scotia
            projection_scale=5,  # Adjust zoom
        )
    )

    fig.show()


    # --- 8. Sunburst Chart Showing Hierarchical Region/Type/Beach Colour (Plotly) ---
    fig = px.sunburst(df, path=['Region', 'Type', 'Beach colour'],
                      title="Hierarchical Sunburst of Beach Characteristics")
    fig.show()

    # --- 9. Correlation Heatmap with Values ---
    numerical_data = df.select_dtypes(include=['number'])
    correlation_matrix = numerical_data.corr()
    plt.figure(figsize=(12, 10))  # adjust as necessary
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix of Numerical Data")
    plt.show()
# --- Main Execution ---
if __name__ == "__main__":
    generate_unique_visualizations(df.copy())