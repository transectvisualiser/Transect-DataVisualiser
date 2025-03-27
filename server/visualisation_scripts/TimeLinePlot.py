import json
import pandas as pd
import plotly.express as px

# Load the JSON file
file_path = "./data/weather-everyday.json"  
with open(file_path, "r") as f:
    data = json.load(f)


df = pd.json_normalize(data, 'observations')


df["obsTimeLocal"] = pd.to_datetime(df["obsTimeLocal"])


fig = px.line(
    df, 
    x="obsTimeLocal", 
    y="metric.tempAvg", 
    title="Temperature Over Time",
    labels={"obsTimeLocal": "Time", "metric.tempAvg": "Temperature (°C)"},
    markers=True
)


fig.show()
