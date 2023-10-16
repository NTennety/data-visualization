import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Read the data
df = pd.read_csv("annual_aqi_by_county_2022.csv")
df2 = df.groupby('State')[['Median AQI' , 'Max AQI', '90th Percentile AQI']].mean().reset_index()


# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

# Define the layout
app.layout = dbc.Container([
    dcc.Markdown("Web Application for Visualizing AQI Index by State"),
        dcc.Dropdown(
        id = 'y-axis',
        options = [{'label': '90th Percentile AQI', 'value' : '90th Percentile AQI'}, {'label' : 'Max AQI', 'value' : 'Max AQI'}],
        value = 'Median AQI',
        clearable = False
    ),
    dcc.Dropdown(
        id='plot-type',
        options=[{'label': 'Bar Plot', 'value': 'Bar Plot'}, {'label': 'Scatter Plot', 'value': 'Scatter Plot'}],
        value='Bar Plot',
        clearable=False
    ),
    dcc.Graph(id='aqi-graph')
])

@app.callback(
    Output('aqi-graph', 'figure'),
    Input('plot-type', 'value'),
    Input('y-axis', 'value')
)
def update_graph(plot_type, y_axis):
    if plot_type == 'Bar Plot':
        figure = px.bar(data_frame=df2, x='State', y=y_axis, title='Average Median AQI by State')
    elif plot_type == 'Scatter Plot':
        figure = px.scatter(data_frame=df2, x='State', y=y_axis, title='Average Median AQI by State')
    return figure

if __name__ == '__main__':
    app.run_server(port=8051)
