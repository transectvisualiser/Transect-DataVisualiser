from flask import Flask, jsonify
from flask_cors import CORS
import plotly
import json
import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Initialize Flask app
app = Flask(__name__)
CORS(app)

from visualisation_scripts.visualization_functions import (
    create_scatter_plot,
    create_box_plot,
    create_litter_histogram,
    create_beach_width_bar_chart,
    create_dune_polar_chart,
    create_sediment_bar_chart,
    create_dendrogram_chart,
    create_cliff_height_dendrogram,
    create_dunes_dendrogram,
    create_vegetation_cover_dendrogram,
    create_density_map,
    create_rose_diagram,
    create_text_table,
    create_time_plot,
    create_sediment_plot,
    create_temperature_plot,
    create_stream_graph,
    create_beach_profile_heatmap
)

@app.route('/plots/scatter', methods=['GET'])
def get_scatter_plot():
    try:
        fig = create_scatter_plot()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)
    except Exception as e:
        print(f"Error creating scatter plot: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/plots/box', methods=['GET'])
def get_box_plot():
    fig = create_box_plot()
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify(graphJSON)

@app.route('/debug/columns', methods=['GET'])
def get_columns():
    try:
        df = pd.read_csv('visualisation_scripts/General List (CSES-NS-Summary-Evaluations).csv')
        return jsonify({"columns": list(df.columns)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/plots/litter', methods=['GET'])
def get_litter_histogram():
    try:
        fig = create_litter_histogram()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)
    except Exception as e:
        print(f"Error creating litter histogram: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/plots/beach_width', methods=['GET'])
def get_beach_width_chart():
    try:
        fig = create_beach_width_bar_chart()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)
    except Exception as e:
        print(f"Error creating beach width bar chart: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/plots/dunes', methods=['GET'])
def get_dune_polar_chart():
    try:
        fig = create_dune_polar_chart()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)
    except Exception as e:
        print(f"Error creating dune polar chart: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/plots/sediment', methods=['GET'])
def get_sediment_chart():
    try:
        fig = create_sediment_bar_chart()  
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)
    except Exception as e:
        print(f"Error creating sediment bar chart: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/plots/dendrogram', methods=['GET'])
def get_dendrogram_chart():
    try:
        fig = create_dendrogram_chart()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)
    except Exception as e:
        print(f"Error creating dendrogram chart: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/plots/cliff_height_dendrogram', methods=['GET'])
def get_cliff_height_dendrogram():
    try:
        fig = create_cliff_height_dendrogram()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)
    except Exception as e:
        print(f"Error creating cliff height dendrogram: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/plots/dunes_dendrogram', methods=['GET'])
def get_dunes_dendrogram():
    try:
        fig = create_dunes_dendrogram()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)
    except Exception as e:
        print(f"Error creating dunes dendrogram: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/plots/vegetation_cover_dendrogram', methods=['GET'])
def get_vegetation_cover_dendrogram():
    try:
        fig = create_vegetation_cover_dendrogram()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)
    except Exception as e:
        print(f"Error creating vegetation cover dendrogram: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/plots/density', methods=['GET'])
def get_density_map():
    """Returns the interactive density map"""
    try:
        fig = create_density_map()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)
    except Exception as e:
        print(f"Error creating density map: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/plots/rose', methods=['GET'])
def get_rose_diagram():
    try:
        fig = create_rose_diagram()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)
    except Exception as e:
        print(f"Error creating rose diagram: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/plots/text', methods=['GET'])
def get_text_table():
    try:
        fig = create_text_table()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)
    except Exception as e:
        print(f"Error creating text table: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/plots/sediment-distribution', methods=['GET'])
def get_sediment_distribution():
    try:
        fig = create_sediment_plot()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)
    except Exception as e:
        print(f"Error creating sediment distribution: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/plots/time', methods=['GET'])
def get_time_plot():
    try:
        fig = create_time_plot()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)
    except Exception as e:
        print(f"Error creating time plot: {str(e)}")
        return jsonify({"error": str(e)}), 500
    

@app.route('/plots/stream', methods=['GET'])
def get_stream_graph():
    try:
        fig = create_stream_graph()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)
    except Exception as e:
        print(f"Error creating text table: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/plots/temperature', methods=['GET'])
def get_temperature_plot():
    try:
        fig = create_temperature_plot()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)
    except Exception as e:
        print(f"Error creating temperature plot: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/plots/heatmap', methods=['GET'])
def get_beach_profile_heatmap():
    try:
        fig = create_beach_profile_heatmap()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)
    except Exception as e:
        print(f"Error creating beach profile heatmap: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return 'Transect Visualizer Backend is running!'

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))  # Fallback to 5001 locally
    app.run(host='0.0.0.0', port=port)



