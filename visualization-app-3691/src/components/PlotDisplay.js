import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';

function PlotDisplay({ plotType }) {
    const [plotData, setPlotData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchPlot = async () => {
            try {
                setLoading(true);
                const response = await fetch(`http://localhost:5001/plots/${plotType}`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                if (!data) {
                    throw new Error('No data received from server');
                }
                setPlotData(JSON.parse(data));
            } catch (err) {
                console.error('Fetch error:', err);
                setError(`Failed to load plot: ${err.message}`);
            } finally {
                setLoading(false);
            }
        };

        fetchPlot();
    }, [plotType]);

    if (loading) return <div>Loading plot...</div>;
    if (error) return <div className="error-message">{error}</div>;
    if (!plotData) return null;

    return (
        <Plot
        data={plotData.data}
        layout={{
          ...plotData.layout,
          autosize: true,
          margin: { t: 40, b: 40, l: 40, r: 20 }, // optional: add some margin
        }}
        config={{
          responsive: true,
          ...plotData.config,
        }}
        useResizeHandler={true}
        // Make the chart fill the parent container
        style={{ width: '100%', height: '100%' }}
      />
    );
}

export default PlotDisplay;