import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize



file_path = "General List (CSES-NS-Summary-Evaluations).csv"
df = pd.read_csv(file_path, na_values=[], keep_default_na=False)

# Create a GeoDataFrame using longitude and latitude
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["Longitude"], df["Latitude"]))
gdf.crs = "EPSG:4326"
gdf = gdf.to_crs(epsg=3857)

# 1. Marker Size: Scale by "Beach width"
gdf["Beach width"] = pd.to_numeric(gdf["Beach width"], errors="coerce")
size_scale = 40
gdf["sizes"] = gdf["Beach width"] * size_scale

# 2. Marker Color: Use "CSES Label"
gdf["CSES_code"] = pd.Categorical(gdf["CSES Label"]).codes



# 3. Marker Shape: Map the "Park" attribute to a marker symbol.
park_markers = {"N/A": "o", "Provincial park": "^", "National park": "s"}





fig, ax = plt.subplots(figsize=(12, 12))

# Plot by grouping on the "Park" attribute so that each group uses its own marker shape
for park_type, group in gdf.groupby("Park"):
    marker = park_markers.get(park_type, "o")
    sc = ax.scatter(
        group.geometry.x,
        group.geometry.y,
        s=group["sizes"],
        c=group["CSES_code"],
        cmap="viridis",
        marker=marker,
        alpha=0.7,
        edgecolor="k",
        label=park_type
    )

# Add a basemap for geographic context
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

# Title and axis labels
ax.set_title("Beaches in Nova Scotia\nSize = Beach Width | Color = CSES Label | Marker = Park Status", fontsize=14)
ax.set_xlabel("Easting")
ax.set_ylabel("Northing")

# Create a colorbar for the CSES Label
norm = Normalize(vmin=gdf["CSES_code"].min(), vmax=gdf["CSES_code"].max())
sm = ScalarMappable(norm=norm, cmap="viridis")
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, fraction=0.016, pad=0.04)

# Set ticks to show the original CSES Label categories
categ = gdf["CSES Label"].astype("category").cat.categories
tick_locs = np.linspace(gdf["CSES_code"].min(), gdf["CSES_code"].max(), len(categ))
cbar.set_ticks(tick_locs)
cbar.set_ticklabels(categ)
cbar.set_label("CSES Label")

plt.legend(title="Park", loc="upper right")
plt.show()
