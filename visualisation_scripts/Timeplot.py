import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Read CSV 
Air_Tempeture = pd.read_csv("visualisation_scripts/Date_Timeplot (4).csv")
Air_Tempeture["Time"] = pd.to_datetime(Air_Tempeture["Time"], format="%I:%M %p")

# Temp dew to numeric 
Air_Tempeture["Temperature(C)"] = (
    Air_Tempeture["Temperature(C)"]
    .astype(str)
    .str.replace("°C", "", regex=True)
    .astype(float)
)

Air_Tempeture["Dew Point (C)"] = (
    Air_Tempeture["Dew Point (C)"]
    .astype(str)
    .str.replace("°C", "", regex=True)
    .astype(float)
)

# Time index 
Air_Tempeture.set_index("Time", inplace=True)

plt.figure(figsize=(12, 5))

# Temp plot 
plt.plot(Air_Tempeture.index, Air_Tempeture["Temperature(C)"], marker="o", linestyle="-", color="b", label="Temperature (°C)")

# dew plot 
plt.plot(Air_Tempeture.index, Air_Tempeture["Dew Point (C)"], marker="o", linestyle="-", color="r", label="Dew Point (°C)")

# x axis 
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%I:%M %p"))

plt.xlabel("Time of Day")
plt.ylabel("Temperature (°C) / Dew Point (°C)")
plt.title("Temperature & Dew Point Trend Throughout the Day")
plt.xticks(rotation=45)  
plt.grid(True)
plt.legend()  

# show Graph 
plt.show()

