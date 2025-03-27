import plotly.express as px
import pandas as pd
import os
import numpy as np  
import plotly.graph_objects as go
import plotly.figure_factory as ff
from scipy.cluster.hierarchy import dendrogram, linkage
import json
from scipy.interpolate import make_interp_spline


# Define file path dynamically
csv_path = os.path.join(os.path.dirname(__file__), "General List (CSES-NS-Summary-Evaluations).csv")

# Load dataset
try:
    df = pd.read_csv(csv_path)
except Exception as e:
    print(f"Error loading CSV file: {str(e)}")
    df = None  # Prevent further processing if loading fails

def validate_dataframe(required_columns):
    """Helper function to check if required columns exist in the dataframe."""
    if df is None:
        raise ValueError("Dataframe is not loaded due to previous errors.")
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

def create_scatter_plot():
    """Creates an interactive scatter plot of beach characteristics"""    
    validate_dataframe(['Cliff height', 'Vegetation cover', 'Region'])
    
    fig = px.scatter(df, 
                    x='Cliff height',
                    y='Vegetation cover',
                    color='Region',
                    title='Beach Characteristics')
    return fig

def create_box_plot():
    """Creates an interactive box plot of cliff heights by region"""
    validate_dataframe(['Region', 'Cliff height'])

    fig = px.box(df,
                 x='Region',
                 y='Cliff height',
                 title='Cliff Height Distribution by Region')
    return fig

def create_bar_chart():
    """Creates an interactive bar chart of average beach width by region"""
    try:
        validate_dataframe(['Region', 'Beach width'])
        
        grouped_data = df.groupby('Region')['Beach width'].agg(['mean', 'count']).reset_index()
        
        fig = px.bar(grouped_data,
                    x='Region',
                    y='mean',
                    title='Average Beach Width by Region',
                    labels={'mean': 'Average Beach Width'})
        return fig
        
    except Exception as e:
        print(f"Error in create_bar_chart: {str(e)}")
        raise

def create_litter_histogram():
    """Creates an interactive histogram of litter levels across beaches."""
    try:
        validate_dataframe(['Beach', 'Litter'])
        
        # Extract relevant data
        df_filtered = df[['Beach', 'Litter']].dropna()
        litter_data = df_filtered["Litter"].tolist()

        # Determine bins dynamically
        expected_levels = {1, 2, 3, 4, 5}
        unique_levels = set(litter_data)
        missing_count = len(expected_levels - unique_levels)
        bins = max(1, 5 - missing_count)  # Ensure at least 1 bin

        # Create interactive Plotly Histogram
        fig = px.histogram(df_filtered, 
                           x="Litter", 
                           nbins=bins, 
                           title="Litter Distribution Level Across Beaches",
                           labels={"Litter": "Litter Level"},
                           opacity=0.7,
                           color_discrete_sequence=["#007bff"])  # Custom color

        # Update layout for better readability
        fig.update_layout(
            xaxis=dict(tickmode="array", tickvals=[1, 2, 3, 4, 5]),
            yaxis_title="Number of Beaches",
            bargap=0.2
        )

        return fig
    
    except Exception as e:
        print(f"Error in create_litter_histogram: {str(e)}")
        raise

def create_beach_width_bar_chart():
    """Creates an interactive bar chart of average beach width by region."""
    try:
        validate_dataframe(['Region', 'Beach width'])
        
        # Group data by region and calculate average beach width
        grouped_data = df.groupby("Region")["Beach width"].mean().reset_index()

        # Create an interactive bar chart
        fig = px.bar(grouped_data,
                    x="Region",
                    y="Beach width",
                    title="Average Beach Width by Region",
                    labels={"Beach width": "Average Beach Width"},
                    color="Region",
                    color_discrete_sequence=px.colors.qualitative.Set1)  # Custom colors

        # Adjust layout
        fig.update_layout(
            xaxis_title="Region",
            yaxis_title="Average Beach Width",
            bargap=0.2,
            xaxis=dict(tickangle=30)
        )

        return fig
    
    except Exception as e:
        print(f"Error in create_beach_width_bar_chart: {str(e)}") 
        raise

def create_dune_polar_chart():
    """Creates an enhanced circular bar plot with individual legends for each region."""
    try:
        validate_dataframe(['Dunes', 'Region'])

        df['Dunes'] = df['Dunes'].astype(float)

        # Calculate average dunes per region
        region_avg = df.groupby('Region')['Dunes'].mean().reset_index()
        region_avg = region_avg.sort_values('Dunes', ascending=False)

        regions = region_avg['Region']
        avg_dunes = region_avg['Dunes']

        N = len(regions)
        angles = np.linspace(0, 360, N, endpoint=False)

        # Normalize bar heights
        max_dunes = avg_dunes.max()
        min_dunes = avg_dunes.min()
        bar_heights = (avg_dunes - min_dunes) / (max_dunes - min_dunes) * 2
        bar_heights = bar_heights.apply(lambda x: 0.2 if x == 0 else x)

        inner_radius = 1.2

        # Define region colors
        region_colors = {
            'Cape Breton': '#1f77b4',
            'Eastern Shore': '#ff7f0e',
            'Halifax': '#2ca02c',
            'North Shore': '#d62728',
            'South Shore': '#9467bd',
            'Yarmouth & Bay of Fundy': '#8c564b'
        }

        fig = go.Figure()

        # Add each region as a separate trace for correct legend entries
        for i, (region, angle, height, dune) in enumerate(zip(regions, angles, bar_heights, avg_dunes)):
            fig.add_trace(go.Barpolar(
                r=[height + inner_radius],
                theta=[angle],
                text=[f"{region}: {dune:.2f}"],
                hoverinfo="text",
                width=[30],
                marker=dict(
                    color=region_colors.get(region, 'gray'),
                    line=dict(color="black", width=1)
                ),
                name=region  # Legend entry per region
            ))

            # Add label above each bar
            angle_rad = np.deg2rad(angle)
            fig.add_annotation(
                x=(height + inner_radius + 0.2) * np.cos(angle_rad),
                y=(height + inner_radius + 0.2) * np.sin(angle_rad),
                text=f"{region}<br>{dune:.2f}",
                showarrow=False,
                font=dict(size=10, color="black"),
                xref="x", yref="y"
            )

        # Layout with proper legend
        fig.update_layout(
            title="Average Dunes by Region (Circular Plot)",
            polar=dict(
                radialaxis=dict(showticklabels=False, showgrid=False, range=[0, inner_radius + 2.5]),
                angularaxis=dict(showgrid=False, showticklabels=False),
            ),
            showlegend=True,
            legend_title="Regions",
            margin=dict(l=50, r=50, t=80, b=120)
        )

        # Bottom-left annotation
        fig.add_annotation(
            text=f"Regions: {N}<br>Overall Avg Dunes: {df['Dunes'].mean():.2f}",
            xref="paper", yref="paper",
            x=0, y=-0.25,
            showarrow=False,
            font=dict(size=12),
            bgcolor="white",
            bordercolor="black",
            borderwidth=1
        )

        return fig

    except Exception as e:
        print(f"Error in create_dune_polar_chart: {str(e)}")
        raise

def create_sediment_bar_chart():
    """Creates an interactive bar chart showing beaches by sediment type and region."""
    try:
        validate_dataframe(['Beach', 'Region', 'Type of sediment'])

        # Filter and count unique beaches per sediment type and region
        df_filtered = df[['Beach', 'Region', 'Type of sediment']].dropna()
        sediment_counts = df_filtered.groupby(['Type of sediment', 'Region'])['Beach'].nunique().unstack(fill_value=0)

        # Create an interactive grouped bar chart
        fig = go.Figure()

        # Define correct color scale for regions
        colors = px.colors.sequential.Plasma  

        for i, region in enumerate(sediment_counts.columns):
            fig.add_trace(go.Bar(
                x=sediment_counts.index,
                y=sediment_counts[region],
                name=region,
                marker_color=colors[i % len(colors)]  # Assign unique colors
            ))

        # Improve layout for clarity
        fig.update_layout(
            title="Beaches by Sediment Type and Region",
            xaxis_title="Type of Sediment",
            yaxis_title="Number of Distinct Beaches",
            barmode="group",  # ✅ Grouped bars instead of stacked
            legend_title="Region",
            xaxis=dict(tickangle=45),  # Rotate x-axis labels for better readability
        )

        return fig

    except Exception as e:
        print(f"Error in create_sediment_bar_chart: {str(e)}")
        raise

def create_dendrogram_chart():
    """Creates an interactive dendrogram of regions based on the average Beach width."""
    try:
        validate_dataframe(['Region', 'Beach width'])

        # Group by Region and compute average beach width
        env_features = ['Beach width']
        region_means = df.groupby('Region')[env_features].mean().dropna()

        # Ensure there are enough regions for clustering
        if len(region_means) < 2:
            raise ValueError("Not enough regions to perform clustering. At least two are required.")

        # Perform hierarchical clustering
        X = region_means.to_numpy()
        labels = region_means.index.tolist()
        Z = linkage(X, method='ward')

        # Create dendrogram using Plotly's built-in figure factory
        fig = ff.create_dendrogram(X, orientation='top', labels=labels, linkagefun=lambda x: Z)

        # Update layout for aesthetics
        fig.update_layout(
            title="Region Clustering (Dendrogram)",
            title_font=dict(size=24),
            xaxis_title="Regions",
            yaxis_title="Distance (Ward's Method)",
            height=600,
            margin=dict(l=50, r=50, t=80, b=150),
        )

        # Improve tick font and angle
        fig.update_xaxes(tickangle=45, tickfont=dict(size=12))
        fig.update_yaxes(tickfont=dict(size=12))

        return fig

    except Exception as e:
        print(f"Error in create_dendrogram_chart: {str(e)}")
        raise

def create_cliff_height_dendrogram():
    """Creates an interactive dendrogram of regions based on the average Cliff height."""
    try:
        validate_dataframe(['Region', 'Cliff height'])

        env_features = ['Cliff height']
        region_means = df.groupby('Region')[env_features].mean().dropna()

        if len(region_means) < 2:
            raise ValueError("Not enough regions to perform clustering. At least two are required.")

        X = region_means.to_numpy()
        labels = region_means.index.tolist()
        Z = linkage(X, method='ward')

        fig = ff.create_dendrogram(X, orientation='top', labels=labels, linkagefun=lambda x: Z)

        fig.update_layout(
            title="Region Clustering Based on Average Cliff Height",
            title_font=dict(size=24),
            xaxis_title="Regions",
            yaxis_title="Distance (Ward's Method)",
            height=600,
            margin=dict(l=50, r=50, t=80, b=150),
        )

        fig.update_xaxes(tickangle=45, tickfont=dict(size=12))
        fig.update_yaxes(tickfont=dict(size=12))

        return fig

    except Exception as e:
        print(f"Error in create_cliff_height_dendrogram: {str(e)}")
        raise

def create_dunes_dendrogram():
    """Creates an interactive dendrogram of regions based on the average Dunes."""
    try:
        validate_dataframe(['Region', 'Dunes'])

        env_features = ['Dunes']
        region_means = df.groupby('Region')[env_features].mean().dropna()

        if len(region_means) < 2:
            raise ValueError("Not enough regions to perform clustering. At least two are required.")

        X = region_means.to_numpy()
        labels = region_means.index.tolist()
        Z = linkage(X, method='ward')

        fig = ff.create_dendrogram(X, orientation='top', labels=labels, linkagefun=lambda x: Z)

        fig.update_layout(
            title="Region Clustering Based on Average Dunes",
            title_font=dict(size=24),
            xaxis_title="Regions",
            yaxis_title="Distance (Ward's Method)",
            height=600,
            margin=dict(l=50, r=50, t=80, b=150),
        )

        fig.update_xaxes(tickangle=45, tickfont=dict(size=12))
        fig.update_yaxes(tickfont=dict(size=12))

        return fig

    except Exception as e:
        print(f"Error in create_dunes_dendrogram: {str(e)}")
        raise

def create_vegetation_cover_dendrogram():
    """Creates an interactive dendrogram of regions based on the average Vegetation cover."""
    try:
        validate_dataframe(['Region', 'Vegetation cover'])

        env_features = ['Vegetation cover']
        region_means = df.groupby('Region')[env_features].mean().dropna()

        if len(region_means) < 2:
            raise ValueError("Not enough regions to perform clustering. At least two are required.")

        X = region_means.to_numpy()
        labels = region_means.index.tolist()
        Z = linkage(X, method='ward')

        fig = ff.create_dendrogram(X, orientation='top', labels=labels, linkagefun=lambda x: Z)

        fig.update_layout(
            title="Region Clustering Based on Average Vegetation Cover",
            title_font=dict(size=24),
            xaxis_title="Regions",
            yaxis_title="Distance (Ward's Method)",
            height=600,
            margin=dict(l=50, r=50, t=80, b=150),
        )

        fig.update_xaxes(tickangle=45, tickfont=dict(size=12))
        fig.update_yaxes(tickfont=dict(size=12))

        return fig

    except Exception as e:
        print(f"Error in create_vegetation_cover_dendrogram: {str(e)}")
        raise
    
def create_density_map():
    """Creates an interactive density map of beaches"""
    # Read data
    file_path = "visualisation_scripts/General List (CSES-NS-Summary-Evaluations).csv"
    df = pd.read_csv(file_path, na_values=[], keep_default_na=False)
    
    # Convert Beach width to numeric
    df["Beach width"] = pd.to_numeric(df["Beach width"], errors="coerce")
    
    # Create interactive map using Scattermapbox instead of scatter_mapbox
    fig = go.Figure()

    for park_type in df['Park'].unique():
        park_data = df[df['Park'] == park_type]
        
        fig.add_trace(go.Scattermapbox(
            lat=park_data["Latitude"],
            lon=park_data["Longitude"],
            mode='markers',
            marker=dict(
                size=park_data["Beach width"]*2,
                color=pd.factorize(park_data["CSES Label"])[0],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="CSES Classification")
            ),
            text=park_data["Beach"],
            hoverinfo='text',
            name=park_type
        ))

    fig.update_layout(
        title="Interactive Beach Map of Nova Scotia",
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=45, lon=-63),
            zoom=7
        ),
        showlegend=True,
        margin={"r":0,"t":30,"l":0,"b":0}
    )

    return fig

def create_time_plot():
    """Creates an interactive temperature and dew point plot"""
    # Read data
    Air_Temperature = pd.read_csv("visualisation_scripts/Date_Timeplot (4).csv")
    Air_Temperature["Time"] = pd.to_datetime(Air_Temperature["Time"], format="%I:%M %p")
    
    # Convert temperature columns
    for col in ["Temperature(C)", "Dew Point (C)"]:
        Air_Temperature[col] = Air_Temperature[col].str.replace("°C", "").astype(float)
    
    # Create interactive plot
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=Air_Temperature["Time"],
        y=Air_Temperature["Temperature(C)"],
        name="Temperature (°C)",
        mode='lines+markers'
    ))
    
    fig.add_trace(go.Scatter(
        x=Air_Temperature["Time"],
        y=Air_Temperature["Dew Point (C)"],
        name="Dew Point (°C)",
        mode='lines+markers'
    ))
    
    fig.update_layout(
        title="Temperature & Dew Point Trend Throughout the Day",
        xaxis_title="Time of Day",
        yaxis_title="Temperature (°C) / Dew Point (°C)",
        hovermode='x unified',
        height=500
    )
    
    return fig

def create_text_table():
    """Creates an interactive visualization of the text table data"""
    # Read data
    data = pd.read_csv('visualisation_scripts/General List (CSES-NS-Summary-Evaluations).csv')
    columns = ['Region', 'Cliff height', 'Noise disturbance', 'Vegetation cover']
    df = pd.DataFrame(data, columns=columns)

    # Create two subplots
    fig = go.Figure()

    # Add scatter plot
    fig.add_trace(go.Scatter(
        x=df['Cliff height'],
        y=df['Vegetation cover'],
        mode='markers',
        marker=dict(
            color=pd.factorize(df['Region'])[0],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Region')
        ),
        text=df['Region'],
        name='Beach Characteristics'
    ))

    # Update layout
    fig.update_layout(
        title='Beach Characteristics Interactive Visualization',
        xaxis_title='Cliff Height',
        yaxis_title='Vegetation Cover',
        hovermode='closest'
    )

    return fig

def create_sediment_plot():
    """Creates an interactive sediment distribution plot"""
    # Read data
    file_path = "visualisation_scripts/General List (CSES-NS-Summary-Evaluations).csv"
    df = pd.read_csv(file_path)
    
    # Extract and process data
    df_filtered = df[['Beach', 'Region', 'Type of sediment']].dropna()
    sediment_counts = df_filtered.groupby(['Type of sediment', 'Region'])['Beach'].nunique().unstack(fill_value=0)
    
    # Create interactive plot
    fig = go.Figure()
    
    for region in sediment_counts.columns:
        fig.add_trace(go.Bar(
            name=region,
            x=sediment_counts.index,
            y=sediment_counts[region],
            text=sediment_counts[region],
            textposition='auto',
        ))
    
    fig.update_layout(
        title="Beaches by Sediment Type and Region",
        xaxis_title="Type of Sediment",
        yaxis_title="Number of Distinct Beaches",
        barmode='group',
        xaxis_tickangle=-45,
        showlegend=True,
        legend_title="Region",
        height=600
    )
    
    return fig

def create_rose_diagram():
    """Creates an interactive wind rose diagram using Plotly"""
    try:
        # Update the file path to be relative to the script location
        file_path = os.path.join(os.path.dirname(__file__), "..", "data", "weather-everyday.json")
        
        with open(file_path, "r") as f:
            data = json.load(f)

        # Rest of the function remains the same
        wind_dirs = [obs["winddirAvg"] for obs in data["observations"] if "winddirAvg" in obs]
        num_bins = 12
        bins = np.linspace(0, 360, num_bins + 1)
        counts, _ = np.histogram(wind_dirs, bins=bins)
        bin_centers = bins[:-1] + (bins[1] - bins[0])/2

        fig = go.Figure()
        
        fig.add_trace(go.Barpolar(
            r=counts,
            theta=bin_centers,
            width=30,
            name='Wind Direction',
            marker_color='cyan',
            marker_line_color="black",
            marker_line_width=1,
            hovertemplate="Direction: %{theta}°<br>Count: %{r}<extra></extra>"
        ))

        fig.update_layout(
            title="Interactive Wind Rose Diagram",
            polar=dict(
                angularaxis=dict(
                    direction="clockwise",
                    rotation=90
                )
            ),
            showlegend=False
        )

        return fig
    except Exception as e:
        print(f"Error in create_rose_diagram: {str(e)}")
        raise


def create_temperature_plot():
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

    return fig


def create_stream_graph():

    data = json.load( open('data/CoCoRaHS_FullReport.json'))

    df = pd.DataFrame(data)

    df['ObservationDate'] = pd.to_datetime(df['ObservationDate'], errors='coerce')
    df = df.sort_values('ObservationDate')


    def clean_column(col):
        return pd.to_numeric(df[col].replace({'T': 0.1, 'NA': 0, '': 0}), errors='coerce').fillna(0)

    df['TotalPrecipAmt'] = clean_column('TotalPrecipAmt')
    df['NewSnowDepth'] = clean_column('NewSnowDepth')
    df['TotalSnowDepth'] = clean_column('TotalSnowDepth')


    layers = [
        df['TotalPrecipAmt'].values,
        df['NewSnowDepth'].values,
        df['TotalSnowDepth'].values
    ]   
    layers = np.array(layers)  


    total = np.sum(layers, axis=0)
    baseline = np.mean(np.cumsum(layers, axis=0), axis=0) - total / 2

    top_bottom_pairs = []
    current_baseline = baseline.copy()

    for i in range(len(layers)):
        top = current_baseline + layers[i]
        bottom = current_baseline
        top_bottom_pairs.append((bottom.copy(), top.copy()))
        current_baseline = top


    def smooth_line(x, y, points=300):
        x_numeric = (x - x.min()).dt.total_seconds()
        x_new = np.linspace(x_numeric.min(), x_numeric.max(), points)
        spline = make_interp_spline(x_numeric, y, k=3)
        y_smooth = spline(x_new)
        x_smooth = pd.date_range(start=x.min(), end=x.max(), periods=points)
        return x_smooth, y_smooth


    fig = go.Figure()
    x = df['ObservationDate']
    layer_names = ['Total Precipitation', 'Snow Depth', 'Total Snow Depth']

    for i in reversed(range(len(top_bottom_pairs))):
        bottom, top = top_bottom_pairs[i]

        x_smooth, top_smooth = smooth_line(x, top)
        _, bottom_smooth = smooth_line(x, bottom)

        fig.add_trace(go.Scatter(
            x=x_smooth,
            y=top_smooth,
            line=dict(width=0),
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=x_smooth,
            y=bottom_smooth,
            fill='tonexty',
            name=f'{layer_names[i]}',
            line=dict(width=0),
            opacity=0.4,
            hoverinfo='x+y'
        ))


    fig.update_layout(
        title='Snow and Precipitation',
        xaxis_title='Date',
        yaxis_title='Measurements'
    )

    return fig

def create_beach_profile_heatmap():
    """Creates a simplified heatmap visualization of beach profiles"""
    try:
        # Load beach profile data from JSON file
        json_path = os.path.join(os.path.dirname(__file__), "..", "data", "beach-profile.json")
        
        with open(json_path, "r") as f:
            beach_data = json.load(f)
        
        # Extract only the essential data for visualization
        profiles = []
        beaches = []
        
        for beach in beach_data["results"]:
            if not beach.get("BEACH"):
                continue
                
            # Extract only point data
            point_values = []
            for key, value in beach.items():
                if key.startswith("Point_") and isinstance(value, (int, float)) or (isinstance(value, str) and value.replace('.', '', 1).isdigit()):
                    try:
                        point_values.append(float(value))
                    except (ValueError, TypeError):
                        continue
            
            if point_values:  # Only add if we have point data
                beaches.append(beach.get("BEACH", "Unknown Beach"))
                profiles.append(point_values[:10])  # Limit to first 10 points for simplicity
        
        # Ensure all profile arrays have the same length by padding with NaN or zeros
        max_length = max(len(profile) for profile in profiles)
        padded_profiles = []
        
        for profile in profiles:
            # Pad shorter arrays with NaN values
            padded = profile + [float('nan')] * (max_length - len(profile))
            padded_profiles.append(padded)
        
        # Create a simple heatmap with the padded data
        fig = px.imshow(
            padded_profiles,  # Use padded profiles instead of profiles
            y=beaches,
            color_continuous_scale="Viridis",
            labels={"color": "Elevation"},
            title="Beach Profile Elevation"
        )
        
        # Use proper colorbar configuration without titleside
        fig.update_layout(
            xaxis_title="Profile Points",
            yaxis_title="Beach",
            height=600,
            coloraxis_colorbar=dict(
                title="Elevation"  # Simple title without positioning
            )
        )
        
        return fig
    except Exception as e:
        print(f"Error creating beach profile heatmap: {str(e)}")
        raise
