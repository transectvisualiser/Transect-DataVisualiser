import React, { useState } from "react";
import PlotDisplay from "./components/PlotDisplay";
import "./App.css";

const plotKeywords = {
  scatter: "Scatter",
  box: "Box",
  litter: "Histogram",
  beach_width: "Bar",
  dunes: "Circular",
  sediment: "Bar",
  dendrogram: "Clustering",
  density: "Density",
  time: "Time Series",
  text: "Table",
  "sediment-distribution": "Distribution",
  rose: "Wind Rose",
  stream: "Stream Graph",
  temperature: "Temperature Graph",
  heatmap: "Heatmap"
};

function App() {
  const [filterKeyword, setFilterKeyword] = useState("All");
  const [columns, setColumns] = useState(2); // Default to 2 columns
  const handleFilterChange = (event) => {
    setFilterKeyword(event.target.value);
  };

  // Slider callback
  const handleSliderChange = (event) => {
    setColumns(parseInt(event.target.value, 10));
  };

  const uniqueKeywords = ["All", ...new Set(Object.values(plotKeywords))];

  const GAP = 30; 

  const gridColumnStyle = {
    display: "grid",
    gridGap: `${GAP}px`,
    gridTemplateColumns: `repeat(${columns}, calc((100% - (${GAP}px * (${columns} - 1))) / ${columns}))`
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>TranSECT Project Visualizer</h1>
      </header>

      <section className="plot-controls">
        <label htmlFor="plot-filter">Filter by Type: </label>
        <select
          id="plot-filter"
          value={filterKeyword}
          onChange={handleFilterChange}
        >
          {uniqueKeywords.map((keyword) => (
            <option key={keyword} value={keyword}>
              {keyword}
            </option>
          ))}
        </select>

        <div className="column-slider">
          <label htmlFor="column-count-slider">Columns: </label>
          <input
            id="column-count-slider"
            type="range"
            min="1"
            max="5"
            value={columns}
            onChange={handleSliderChange}
          />
          <span className="slider-value">{columns}</span>
        </div>
      </section>

      <section className="visualization-grid" style={gridColumnStyle}>
        {filterKeyword === "All" || plotKeywords["scatter"] === filterKeyword ? (
          <div className="visualization-item">
            <h2>Scatter Plot</h2>
            <PlotDisplay plotType="scatter" />
          </div>
        ) : null}

        {filterKeyword === "All" || plotKeywords["box"] === filterKeyword ? (
          <div className="visualization-item">
            <h2>Box Plot</h2>
            <PlotDisplay plotType="box" />
          </div>
        ) : null}

        {filterKeyword === "All" || plotKeywords["litter"] === filterKeyword ? (
          <div className="visualization-item">
            <h2>Litter Histogram</h2>
            <PlotDisplay plotType="litter" />
          </div>
        ) : null}

        {filterKeyword === "All" || plotKeywords["beach_width"] === filterKeyword ? (
          <div className="visualization-item">
            <h2>Beach Width by Region</h2>
            <PlotDisplay plotType="beach_width" />
          </div>
        ) : null}

        {filterKeyword === "All" || plotKeywords["dunes"] === filterKeyword ? (
          <div className="visualization-item">
            <h2>Dunes by Beach (Circular Plot)</h2>
            <PlotDisplay plotType="dunes" />
          </div>
        ) : null}

        {filterKeyword === "All" || plotKeywords["sediment"] === filterKeyword ? (
          <div className="visualization-item">
            <h2>Beaches by Sediment Type</h2>
            <PlotDisplay plotType="sediment" />
          </div>
        ) : null}

        {filterKeyword === "All" || plotKeywords["dendrogram"] === filterKeyword ? (
          <div className="visualization-item">
            <h2>Region Clustering (Dendrogram)</h2>
            <PlotDisplay plotType="dendrogram" />
          </div>
        ) : null}

        {filterKeyword === "All" || plotKeywords["dunes_dendrogram"] === filterKeyword ? (
         <div className="visualization-item">
             <h2>Region Clustering (Dunes)</h2>
            <PlotDisplay plotType="dunes_dendrogram" />
            </div>
          ) : null}

         {filterKeyword === "All" || plotKeywords["cliff_height_dendrogram"] === filterKeyword ? (
         <div className="visualization-item">
          <h2>Region Clustering (Cliff Height)</h2>
             <PlotDisplay plotType="cliff_height_dendrogram" />
            </div>
          ) : null}

        {filterKeyword === "All" || plotKeywords["vegetation_cover_dendrogram"] === filterKeyword ? (
        <div className="visualization-item">
          <h2>Region Clustering (Vegetation Cover)</h2>
          <PlotDisplay plotType="vegetation_cover_dendrogram" />
           </div>
         ) : null}



        {filterKeyword === "All" || plotKeywords["density"] === filterKeyword ? (
          <div className="visualization-item">
            <h2>Density Map</h2>
            <PlotDisplay plotType="density" />
          </div>
        ) : null}

        {filterKeyword === "All" || plotKeywords["time"] === filterKeyword ? (
          <div className="visualization-item">
            <h2>Temperature Trends</h2>
            <PlotDisplay plotType="time" />
          </div>
        ) : null}

        {filterKeyword === "All" || plotKeywords["text"] === filterKeyword ? (
          <div className="visualization-item">
            <h2>Beach Characteristics Table</h2>
            <PlotDisplay plotType="text" />
          </div>
        ) : null}

        {filterKeyword === "All" ||
        plotKeywords["sediment-distribution"] === filterKeyword ? (
          <div className="visualization-item">
            <h2>Sediment Distribution</h2>
            <PlotDisplay plotType="sediment-distribution" />
          </div>
        ) : null}

        {filterKeyword === "All" || plotKeywords["rose"] === filterKeyword ? (
          <div className="visualization-item">
            <h2>Wind Direction Analysis</h2>
            <PlotDisplay plotType="rose" />
          </div>
        ) : null}

        {filterKeyword === "All" || plotKeywords["temperature"] === filterKeyword ? (
          <div className="visualization-item">
            <h2>Temperature Line Graph</h2>
            <PlotDisplay plotType="temperature"/>
          </div>
        ) : null}

        {filterKeyword === "All" || plotKeywords["stream"] === filterKeyword ? (
          <div className="visualization-item">
            <h2>Stream Graph</h2>
            <PlotDisplay plotType="stream" />
          </div>
        ) : null}

        {filterKeyword === "All" || plotKeywords["heatmap"] === filterKeyword ? (
            <div className="visualization-item">
                <h2>Beach Profile Heatmap</h2>
                <PlotDisplay plotType="heatmap" />
            </div>
        ) : null}
      </section>

      <footer className="app-footer">
        <p>© {new Date().getFullYear()} TranSECT Project Visualizer. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;