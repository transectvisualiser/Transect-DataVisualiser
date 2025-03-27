
def StreamGraph():
    import pandas as pd
    import json
    import numpy as np
    import plotly.graph_objects as go
    from scipy.interpolate import make_interp_spline

    with open('data/CoCoRaHS_FullReport.json') as f:
        data = json.load(f)

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

    fig.show()

StreamGraph()