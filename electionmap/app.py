from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import json

turnout_df = pd.read_csv("/Users/student/Documents/electionmap/2025_Wards_Reporting.csv")
turnout_df["Ward"] = turnout_df["Ward"].astype(str)

poll_df = pd.read_csv("/Users/student/Documents/electionmap/polling_places.csv")

with open("/Users/student/Documents/electionmap/Political_Wards.geojson") as f:
    wards_geo = json.load(f)

app = Dash(__name__)

def update_map(colorscale, show_polling):
    fig = px.choropleth_map(
        turnout_df,
        geojson=wards_geo,
        locations="Ward",
        featureidkey="properties.ward_num",
        color="Percent Turnout",
        color_continuous_scale=colorscale,
        map_style="carto-positron",
        center={"lat": 40.005, "lon": -75.13},
        zoom=9.5,
        height=800,
        width=800,
    )

    if "show" in show_polling:
        fig_poll = px.scatter_map(
            poll_df,
            lat="lat",
            lon="lng",
            hover_name="placename"
        )

        for trace in fig_poll.data:
            fig.add_trace(trace)

    return fig

app.layout = html.Div([
    html.H2("V5: Interactive Philadelphia 2025 Election: Voter Turnout by Ward"),

    html.Div([
        html.Label("Choose color scale:"),
        dcc.Dropdown(
            id="colorscale",
            options=[{"label": "Reds", "value": "Reds"}, {"label": "Viridis", "value": "Viridis"},
                     {"label": "Blues", "value": "Blues"}, {"label": "Inferno", "value": "Inferno"}],
            value="Reds",
            clearable=False
        ),
    ], style={"width": "300px"}),

    dcc.Checklist(
        id="polling-toggle",
        options=[{"label": "Show Polling Places", "value": "show"}],
        value=["show"]
    ),

    dcc.Graph(id="map", style={"height": "800px", "width": "800px"})
])

@app.callback(
    Output("map", "figure"),
    Input("colorscale", "value"),
    Input("polling-toggle", "value")
)
def update_map_callback(colorscale, show_polling):
    return update_map(colorscale, show_polling)

if __name__ == "__main__":
    app.run(debug=True)
