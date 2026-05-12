# Import packages
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Incorporate data
df = pd.read_csv("Invasive_Species.csv")

DATE_COL = "ObservationDate"
SPECIES_COL = "InvasiveName"
LOCATION_COL = "Town"
AREA_COL = "InfestedArea"

df = df.dropna(subset=[DATE_COL])
locations = sorted(df[LOCATION_COL].dropna().unique())

# Initialize the app
app = Dash()

# Global font for page
GLOBAL_FONT = {
    "fontFamily": "Arial",
    "color": "black",
    "fontSize": "14px"
}

# App layout
app.layout = html.Div([
    html.Div(children='Invasive species', style=GLOBAL_FONT),
    html.Hr(),

    dcc.Dropdown(
        options=[{"label": loc, "value": loc} for loc in locations],
        value=locations[0],
        id='town-dropdown',
        clearable=False,
        style=GLOBAL_FONT
    ),

    html.Br(),

    html.Div([
        dcc.Graph(
            figure={},
            id='species-bar-chart',
            style={"width": "48%", "display": "inline-block"}
        ),
        dcc.Graph(
            figure={},
            id='time-line-chart',
            style={"width": "48%", "display": "inline-block"}
        ),
    ],
    style={
        "display": "flex",
        "justify-content": "space-between",
        "align-items": "center"
    })
], style={**GLOBAL_FONT, "padding": "1.5em"})


# Callback for species bar chart
@callback(
    Output('species-bar-chart', 'figure'),
    Input('town-dropdown', 'value')
)
def update_species_chart(town):
    dff = df[df[LOCATION_COL] == town]

    species_area = (
        dff.groupby(SPECIES_COL)[AREA_COL]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        species_area,
        x=SPECIES_COL,
        y=AREA_COL,
        title=f"Total Infestation by Species in {town}",
        hover_data=[AREA_COL]
    )

    # Smaller graph fonts here
    fig.update_layout(
        xaxis_title="Species",
        yaxis_title="Infested Area",
        font=dict(family="Arial", size=12, color="black"),
        title=dict(font=dict(size=14))
    )
    return fig


# Callback for time series chart
@callback(
    Output('time-line-chart', 'figure'),
    Input('town-dropdown', 'value')
)
def update_time_chart(town):
    dff = df[df[LOCATION_COL] == town]

    time_series = (
        dff.groupby(DATE_COL)[AREA_COL]
        .sum()
        .reset_index()
        .sort_values(DATE_COL)
    )

    fig = px.line(
        time_series,
        x=DATE_COL,
        y=AREA_COL,
        markers=True,
        title=f"Infestation Over Time in {town}",
        hover_data=[AREA_COL]
    )

    # Smaller graph fonts here
    fig.update_layout(
        xaxis_title="Date Observed",
        yaxis_title="Infested Area",
        font=dict(family="Arial", size=12, color="black"),
        title=dict(font=dict(size=14))
    )
    return fig


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
