import React, { useState } from "react";
import PlotDisplay from "./components/PlotDisplay";
import "./App.css";
  
 
const categories = {
  attribute: "Physical Beach Attributes & Morphology",
  sedimentBeach: "Sediment and Beach Type",
  regionalCluster: "Regional Clustering & Grouping",
  mapping: "Spatial and Density Mapping",
  meteorlogicalEnv: "Meterological and Environmental",
  Pollution: "Environmental Impact / Pollution",
  Additional: "Additional Visualizations"
}
 
/*
 
1. Physical Beach Attributes & Morphology
* Overall Attributes: Beach Characteristics, Beach Profile Elevation heat map
* Specific Features: Cliff Height Distribution by Region, Average Beach Width by Region, Dunes by Beach (circular plot), Average Dunes by Region
 
2. Sediment and Beach Type
* Sediment Composition: Beaches by Sediment Type and Region
 
3. Regional Clustering & Grouping
* Clustering Analyses: Region Clustering (dendrogram), Region Clustering based on average Dunes, Region Clustering (Cliff Height)�• Region Clustering (Vegetation Cover)
 
4. Spatial and Density Mapping
* Mapping and Density: Density Map beaches by width
 
5. Meteorological and Environmental Data
* Weather Trends: Temperature & Dew Point Trend Throughout the Day, Temperature over time, Wind Direction Analysis
* Precipitation Patterns: Snow and Precipitation stream graph
 
6. Additional/Interactive Visualizations
* User Interaction & Exploration: Beach Characteristics Interactive Visualization
 
7. Environmental Impact / Pollution
* Pollution Metrics:�• Litter Distribution
 
 
*/
 
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
 
  const allCategories = ["All", ...new Set(Object.values(categories))];
  
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>TranSECT Project Visualizer</h1>
      </header>
 
      <section className="plot-controls" >
        <label htmlFor="plot-filter">Filter by Type: </label>
        <select
          id="plot-filter"
          value={filterKeyword}
          onChange={handleFilterChange}
        >
          {allCategories.map((keyword) => (
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
 
      <section className="visualization-grid">
        {/* Physical Beach Attributes & Morphology */}
        {(filterKeyword === "All" || filterKeyword === categories.attribute) && (
          <div className="visualization-category">
            <h2 className="visualization-category-title">Physical Beach Attributes & Morphology</h2>
            <div className="visualization-items-container" style={{"--columns": columns}}>
              <div className="visualization-item">
                <h2>Scatter Plot</h2>
                <PlotDisplay plotType="scatter" />
              </div>
              <div className="visualization-item">
                <h2>Box Plot</h2>
                <PlotDisplay plotType="box" />
              </div>
              <div className="visualization-item">
                <h2>Beach Width by Region</h2>
                <PlotDisplay plotType="beach_width" />
              </div>
              <div className="visualization-item">
                <h2>Dunes by Beach (Circular Plot)</h2>
                <PlotDisplay plotType="dunes" />
              </div>
              <div className="visualization-item">
                <h2>Beach Profile Heatmap</h2>
                <PlotDisplay plotType="heatmap" />
              </div>
            </div>
          </div>
        )}
 
        {/* Environmental Impact / Pollution */}
        {(filterKeyword === "All" || filterKeyword === categories.Pollution) && (
          <div className="visualization-category">
            <h2 className="visualization-category-title">Environmental Impact / Pollution</h2>
            <div className="visualization-items-container" style={{"--columns": columns}}>
              <div className="visualization-item">
                <h2>Litter Histogram</h2>
                <PlotDisplay plotType="litter" />
              </div>
            </div>
          </div>
        )}
 
        {/* Sediment and Beach Type */}
        {(filterKeyword === "All" || filterKeyword === categories.sedimentBeach) && (
          <div className="visualization-category">
            <h2 className="visualization-category-title">Sediment and Beach Type</h2>
            <div className="visualization-items-container" style={{"--columns": columns}}>
              <div className="visualization-item">
                <h2>Beaches by Sediment Type</h2>
                <PlotDisplay plotType="sediment" />
              </div>
              <div className="visualization-item">
                <h2>Sediment Distribution</h2>
                <PlotDisplay plotType="sediment-distribution" />
              </div>
            </div>
          </div>
        )}
 
        {/* Regional Clustering & Grouping */}
        {(filterKeyword === "All" || filterKeyword === categories.regionalCluster) && (
          <div className="visualization-category">
            <h2 className="visualization-category-title">Regional Clustering & Grouping</h2>
            <div className="visualization-items-container" style={{"--columns": columns}}>
              <div className="visualization-item">
                <h2>Region Clustering (Dendrogram)</h2>
                <PlotDisplay plotType="dendrogram" />
              </div>
              <div className="visualization-item">
                <h2>Region Clustering (Dunes)</h2>
                <PlotDisplay plotType="dunes_dendrogram" />
              </div>
              <div className="visualization-item">
                <h2>Region Clustering (Cliff Height)</h2>
                <PlotDisplay plotType="cliff_height_dendrogram" />
              </div>
              <div className="visualization-item">
                <h2>Region Clustering (Vegetation Cover)</h2>
                <PlotDisplay plotType="vegetation_cover_dendrogram" />
              </div>
            </div>
          </div>
        )}
 
        {/* Spatial and Density Mapping */}
        {(filterKeyword === "All" || filterKeyword === categories.mapping) && (
          <div className="visualization-category">
            <h2 className="visualization-category-title">Spatial and Density Mapping</h2>
            <div className="visualization-items-container" style={{"--columns": columns}}>
              <div className="visualization-item">
                <h2>Density Map</h2>
                <PlotDisplay plotType="density" />
              </div>
            </div>
          </div>
        )}
 
        {/* Meteorological and Environmental */}
        {(filterKeyword === "All" || filterKeyword === categories.meteorlogicalEnv) && (
          <div className="visualization-category">
            <h2 className="visualization-category-title">Meteorological and Environmental</h2>
            <div className="visualization-items-container" style={{"--columns": columns}}>
              <div className="visualization-item">
                <h2>Temperature Trends</h2>
                <PlotDisplay plotType="time" />
              </div>
              <div className="visualization-item">
                <h2>Wind Direction Analysis</h2>
                <PlotDisplay plotType="rose" />
              </div>
              <div className="visualization-item">
                <h2>Stream Graph</h2>
                <PlotDisplay plotType="stream" />
              </div>
              <div className="visualization-item">
                <h2>Temperature Line Graph</h2>
                <PlotDisplay plotType="temperature"/>
              </div>
            </div>
          </div>
        )}
 
        {/* Additional Visualizations */}
        {(filterKeyword === "All" || filterKeyword === categories.Additional) && (
          <div className="visualization-category">
            <h2 className="visualization-category-title">Additional Visualizations</h2>
            <div className="visualization-items-container" style={{"--columns": columns}}>
              <div className="visualization-item">
                <h2>Beach Characteristics Table</h2>
                <PlotDisplay plotType="text" />
              </div>
            </div>
          </div>
        )}
      </section>
 
      <footer className="app-footer">
        <p>© {new Date().getFullYear()} TranSECT Project Visualizer. All rights reserved.</p>
      </footer>
    </div>
  );
}
 
export default App;